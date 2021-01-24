import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

import django
django.setup()

import pandas as pd
import numpy as np
from core.models import *
import os
import pytz
#from read_table import *
#from refresh_cars import *
#legenda_contexto = '200'



dic_empresa_cittamobi = {e.nome_cittamobi: e for e in Empresa.objects.all()}  

def create_lines(df):
    print(df.columns)
    df2 = df[['company_name', 'number_line', 'name_line']].drop_duplicates()
    df2 = df2[df2.company_name == 'Empresa São Francisco']
    numeros = Linha.objects.all().values_list('numero', flat=True)
    df2 = df2[~df2.number_line.astype(int).isin(numeros)]
    if df2.empty:
        print('Sem novas linhas')
        return None
    print(df2)
    linhas = np.vectorize(lambda empresa, numero, nome: Linha(nome=nome, numero=numero, empresa=dic_empresa_cittamobi[empresa]))(
        df2['company_name'].values,
        df2['number_line'].values,
        df2['name_line'].values
    )
    Linha.objects.bulk_create(list(linhas))
    print('Linhas Criadas')


def create_pontos(df):
    trechos_dict = {t.nome: t for t in Trecho.objects.all()}
    trechos = list(np.array([t for t in df.TRECHO.unique() if not t in list(trechos_dict.keys())]))
    if trechos:
        trechos = np.vectorize(lambda x: Trecho(nome=x))(trechos)
        Trecho.objects.bulk_create(list(trechos))
        trechos_dict = {t.nome: t for t in Trecho.objects.all()}
    if not Ponto.objects.all().exists():
        print(df.LAT.astype(float).values)
        df = df.drop_duplicates(subset=['company', 'stop_id'])
        pontos = np.vectorize(lambda lat, lon, trecho, endereco, codigo, bairro: Ponto(
            lat = lat,
            lon = lon,
            trecho = trechos_dict[trecho],
            endereco = endereco,
            endereco_cittamobi = endereco,
            endereco_unico = False,
            codigo = codigo,
            bairro = bairro
        ))(
            df.LAT.astype(float).values,
            df.LON.astype(float).values,
            df.TRECHO.values,
            df.adress.values,
            df.stop_id.values,
            df.bairro.values,
        )
        Ponto.objects.bulk_create(list(pontos))
    if not PontoPorEmpresa.objects.all().exists():
        pontos = {p.codigo: p for p in Ponto.objects.all()}
        ppe = np.vectorize(lambda p, e, c: PontoPorEmpresa(
            ponto = pontos[p],
            empresa=dic_empresa_cittamobi[e],
            codigo_cittamobi=c

        ))(
            df.stop_id.values,
            df.company.values,
            df.stop_id.values,
        )
        PontoPorEmpresa.objects.bulk_create(list(ppe))



def create_viagens(df):
    dic_linhas = {int(l.numero): l for l in Linha.objects.all()}
    dic_carros = {c.numero: c for c in Carro.objects.all()}

    df1 = df[~df.linha.isna()]
    df2 = df1.drop_duplicates(['LINHA', 'CARRO', 'partida_prevista'])
    maceio_tz = pytz.timezone("UTC")
    hora_or_none = lambda x: maceio_tz.localize(pd.to_datetime(x)) if not x is None else x

    Partida.objects.all().delete()
    partidas = np.vectorize(lambda linha, atendimento, carro, partida_prevista, partida_realizada, sentido: Partida(
        linha=dic_linhas[int(linha)],
        atendimento=atendimento,
        carro=dic_carros[str(carro)],
        horario_prevista_terminal=hora_or_none(partida_prevista),
        horario_realizada_terminal=hora_or_none(partida_realizada),
        sentido=sentido,
        
    ))(
        df2.LINHA.values,
        df2.linha.values,
        df2.CARRO.values,
        df2.partida_prevista.values,
        df2.partida_realizada.values,
        df2.sentido.values,
    )
    Partida.objects.bulk_create(list(partidas))
    print('Partidas Criadas')


    dic_partidas = {(int(p.linha.numero), p.carro.numero, pd.to_datetime(p.horario_prevista_terminal).strftime('%d/%m/%Y'), pd.to_datetime(p.horario_prevista_terminal).strftime('%H:%M')):p for p in Partida.objects.select_related().all()}
    print(list(dic_partidas.keys())[0])
    cartoes_existentes = Cartao.objects.all().values_list('numero', flat=True)
    df1_ = df[~df.CARTAO.isin(cartoes_existentes)]
    if not df1_.empty:
        tipos = df1_.TIPO.unique()
        from core.models import TipoCartao
        tipos_existentes = TipoCartao.objects.all().values_list('tipo', flat=True)
        df1__ = df1_[~df1_['TIPO'].isin(tipos_existentes)]
        if not df1__.TIPO.empty:
            tipos = np.vectorize(lambda numero: TipoCartao(
                tipo=numero,
                valor=0,
            ))(
                df1__.TIPO.unique(),
            )
            TipoCartao.objects.bulk_create(list(tipos))
        dic_tipos = {tipo.tipo: tipo for tipo in TipoCartao.objects.all()}
        df1_ = df1_.drop_duplicates(subset=['CARTAO', 'TIPO'])

        cartoes = np.vectorize(lambda numero, tipo: Cartao(
            numero=numero,
            tipo=dic_tipos[tipo],
        ))(
            df1_.CARTAO.values,
            df1_.TIPO.values,
        )
        Cartao.objects.bulk_create(list(cartoes))
    dic_cartaos = {p.numero:p for p in Cartao.objects.select_related().all()}
    #print(dic_cartaos)
    dic_pontos = {p.codigo_cittamobi:p for p in PontoPorEmpresa.objects.select_related().all()}
    print(dic_pontos)
    get__data_str_datetime_or_none = lambda partida: pd.to_datetime(partida).strftime('%d/%m/%Y') if not pd.isnull(partida) else ''
    get__hora_str_datetime_or_none = lambda partida: pd.to_datetime(partida).strftime('%H:%M') if not pd.isnull(partida) else ''
    
    for i, df_ in df.groupby(['LINHA', 'CARRO']):
        print(i)
        viagens = np.vectorize(lambda linha, carro, horario, partida, cartao, ponto_embarque, valor: ViagemDePassageiro(
            linha=dic_linhas[int(linha)],
            partida_embarque=dic_partidas.get((int(linha), str(carro), get__data_str_datetime_or_none(partida), get__hora_str_datetime_or_none(partida))),
            horario=hora_or_none(horario),
            ponto_embarque=dic_pontos.get(ponto_embarque),
            cartao=dic_cartaos[cartao],
            valor=valor
        ))(
            df_.LINHA.values,
            df_.CARRO.values,
            df_.HORARIO.values,
            df_.partida_prevista.values,
            df_.CARTAO.values,
            df_.station.values,
            df_.VALOR.values
        )


        ViagemDePassageiro.objects.bulk_create(list(viagens))
        print('Criou')

    

dfs = []
df_tvs = []
for legenda_contexto in ['200', '3 a 10-10-2020']:
    pre = '../Resultados/'+legenda_contexto+'/'
    pos = ''
    #MAIN
    df_tvs.append(pd.read_pickle(pre + 'departures total'+ pos +'.zip', compression='zip'))
    
    arquivos = [pre + 'PassageirosPorPonto/'+f for f in os.listdir(pre + 'PassageirosPorPonto/') if f.endswith('.zip')]

    print(arquivos)
    for a in arquivos:
        df = pd.read_pickle(a, compression='zip')
        dfs.append(df)





df_tv = pd.concat(df_tvs, ignore_index=True)

create_lines(df_tv)
df_pontos = pd.read_excel('../ScriptsIniciais/base_pontos'+ pos +'.xlsx', engine='openpyxl')
print(df_pontos)
create_pontos(df_pontos)
print('Pontos Criados')

df_pass = pd.concat(dfs, ignore_index=True)
dfs = None
df = None

print(len(df_pass.partida_prevista.unique()))
print(df_pass.count())
df_pass.linha


 
create_viagens(df_pass)
print('Dados de passageiros finalizados')
print('Criando ordem dos pontos')
#from read_stop_orders import *
print('\n\n\n\n------------------\n\nFinalizado!\n')
