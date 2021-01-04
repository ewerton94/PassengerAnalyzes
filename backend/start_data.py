import pandas as pd
import numpy as np
from core.models import *
import os
import pytz
#from read_table import *
#from refresh_cars import *
#legenda_contexto = '200'
legenda_contexto = '3 a 10-10-2020'

pre = '../Resultados/'+legenda_contexto+'/'
pos = ''


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

    #Partida.objects.all().delete()
    partidas = np.vectorize(lambda linha, atendimento, carro, partida_prevista, partida_realizada, sentido: Partida(
        linha=dic_linhas[int(linha)],
        atendimento=atendimento,
        carro=dic_carros[str(carro)],
        horario_prevista_terminal=maceio_tz.localize(pd.to_datetime(partida_prevista)),
        horario_realizada_terminal=maceio_tz.localize(pd.to_datetime(partida_realizada)),
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


    dic_partidas = {(int(p.linha.numero), p.carro.numero, pd.to_datetime(p.horario_prevista_terminal).strftime('%d/%m/%Y'), pd.to_datetime(p.horario_prevista_terminal).strftime('%H:%M')):p for p in Partida.objects.select_related().all()}
    print(list(dic_partidas.keys())[0])
    cartoes_existentes = Cartao.objects.all().values_list('numero', flat=True)
    df1_ = df1[~df1.CARTAO.isin(cartoes_existentes)]
    cartoes = np.vectorize(lambda numero: Cartao(
        numero=numero,
        tipo_id=1,
    ))(
        df1_.CARTAO.unique(),
    )
    Cartao.objects.bulk_create(list(cartoes))
    dic_cartaos = {p.numero:p for p in Cartao.objects.select_related().all()}
    #print(dic_cartaos)
    dic_pontos = {p.codigo_cittamobi:p for p in PontoPorEmpresa.objects.select_related().all()}
    print(dic_pontos)
    viagens = np.vectorize(lambda linha, carro, horario, partida, cartao, ponto_embarque, valor: ViagemDePassageiro(
        partida_embarque=dic_partidas.get((int(linha), str(carro), pd.to_datetime(partida).strftime('%d/%m/%Y'), pd.to_datetime(partida).strftime('%H:%M'))),
        horario=maceio_tz.localize(pd.to_datetime(horario)),
        ponto_embarque=dic_pontos.get(ponto_embarque),
        cartao=dic_cartaos[cartao],
        valor=valor
    ))(
        df.LINHA.values,
        df.CARRO.values,
        df.HORARIO.values,
        df.partida_prevista.values,
        df.CARTAO.values,
        df.station.values,
        df.VALOR.values
    )

    ViagemDePassageiro.objects.bulk_create(list(viagens))
    print(ViagemDePassageiro.objects.all())

    





#MAIN
df_tv = pd.read_pickle(pre + 'departures total'+ pos +'.zip', compression='zip')
create_lines(df_tv)
df_pontos = pd.read_excel('../ScriptsIniciais/base_pontos'+ pos +'.xlsx')
print(df_pontos)
create_pontos(df_pontos)
print('Pontos Criados')
arquivos = [pre + 'PassageirosPorPonto/'+f for f in os.listdir(pre + 'PassageirosPorPonto/') if f.endswith('.zip')]
dfs = []
print(arquivos)
for a in arquivos:
    df = pd.read_pickle(a, compression='zip')
    dfs.append(df)
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
