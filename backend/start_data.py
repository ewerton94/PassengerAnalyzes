import pandas as pd
import numpy as np
from core.models import *
#from read_table import *
#from refresh_cars import *

pre = '../Resultados/'
pos = ''


dic_empresa_cittamobi = {e.nome_cittamobi: e for e in Empresa.objects.all()}  

def create_lines(df):
    print(df.columns)
    df2 = df[['company_name', 'number_line', 'name_line']].drop_duplicates()
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
    Linha.objects.bulk_create(linhas)
    print('Linhas Criadas')


def create_pontos(df):
    trechos_dict = {t.nome: t for t in Trecho.objects.all()}
    trechos = np.array([t for t in df.TRECHO.unique() if not t in list(trechos_dict.keys())])
    if trechos:
        trechos = np.vectorize(lambda x: Trecho(nome=x))(trechos)
        Trecho.objects.bulk_create(list(trechos))
        trechos_dict = {t.nome: t for t in Trecho.objects.all()}
    if not Ponto.objects.all().exists():
        print(df.LAT.astype(float).values)
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
    dic_linhas = {l.numero: l for l in Linha.objects.all()}
    dic_carros = {c.numero: c for c in Carro.objects.all()}

    df1 = df[~df.linha.isna()]
    df2 = df1.drop_duplicates(['LINHA', 'CARRO', 'partida'])

    Partida.objects.all().delete()
    partidas = np.vectorize(lambda linha, atendimento, carro, horario, sentido: Partida(
        linha=dic_linhas[str(int(linha))],
        atendimento=atendimento,
        carro=dic_carros[str(carro)],
        horario_prevista_terminal=pd.to_datetime(horario),
        sentido=sentido
    ))(
        df2.LINHA.values,
        df2.linha.values,
        df2.CARRO.values,
        df2.partida.values,
        df2.sentido.values,
    )
    Partida.objects.bulk_create(list(partidas))


    dic_partidas = {(p.linha.numero, p.carro.numero, pd.to_datetime(p.horario_prevista_terminal).date(), pd.to_datetime(p.horario_prevista_terminal).time()):p for p in Partida.objects.select_related().all()}
    print(list(dic_partidas.keys())[0])
    '''
    cartoes = np.vectorize(lambda numero: Cartao(
        numero=numero,
        tipo_id=1,
    ))(
        df1.CARTAO.values,
    )
    Cartao.objects.bulk_create(list(cartoes))
    '''
    dic_cartaos = {p.numero:p for p in Cartao.objects.select_related().all()}
    #print(dic_cartaos)
    dic_pontos = {p.codigo_cittamobi:p for p in PontoPorEmpresa.objects.select_related().all()}
    print(dic_pontos)
    viagens = np.vectorize(lambda linha, carro, horario, partida, cartao, ponto_embarque: ViagemDePassageiro(
        partida_embarque=dic_partidas[(str(int(linha)), str(carro), pd.to_datetime(partida).date(), pd.to_datetime(partida).time())],
        horario=pd.to_datetime(horario),
        ponto_embarque=dic_pontos[ponto_embarque],
        cartao=dic_cartaos[cartao],
    ))(
        df1.LINHA.values,
        df1.CARRO.values,
        df1.HORARIO.values,
        df1.partida.values,
        df1.CARTAO.values,
        df1.station.values,
    )

    ViagemDePassageiro.objects.bulk_create(list(viagens))
    print(ViagemDePassageiro.objects.all())

    





#MAIN
#df_tv = pd.read_pickle(pre + 'departures total'+ pos +'.zip', compression='zip')
#create_lines(df_tv)
#df_pontos = pd.read_excel(pre + '/pontos'+ pos +'.xlsx')
#create_pontos(df_pontos)
df_pass = pd.read_pickle(pre + 'PassageirosPorPonto/passageiros_pontos 0716'+ pos +'.zip', compression='zip')
create_viagens(df_pass)
errrrr
