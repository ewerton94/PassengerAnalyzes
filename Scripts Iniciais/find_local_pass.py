import pandas as pd
from datetime import timedelta, datetime
from numpy import nan
import xlrd
from django.utils import timezone


from os import listdir
import sys
import numpy as np
import json
from collections import OrderedDict, defaultdict

print('AKI')
def get_local_pass(cartao, horario):
        try:
                return LOCAL_FROM_PASS[(cartao, pd.to_datetime(horario))]['stop']
        except:
                return 'erro'
def get_linha_pass(cartao, horario):
        try:
                return LOCAL_FROM_PASS[(cartao, pd.to_datetime(horario))]['linha']
        except:
                return 'erro'

def get_via_pass(cartao, horario):
        try:
                return LOCAL_FROM_PASS[(cartao, pd.to_datetime(horario))]['via']
        except:
                return 'erro'


def get_partida_pass(cartao, horario):
        try:
                return LOCAL_FROM_PASS[(cartao, pd.to_datetime(horario))]['partida']
        except:
                return 'erro'
def get_sentido_pass(cartao, horario):
        try:
                return LOCAL_FROM_PASS[(cartao, pd.to_datetime(horario))]['direction']
        except:
                return 'erro'


def fix_date(df, col):
        df[col] = df[col].astype(object)
        a = df[col].apply(type)
        b = a[a==int]
        c = a[a!=int]
        
        df.loc[b.index, col] = pd.to_datetime(df.loc[b.index, col], unit='ns')
        df.loc[c.index, col] = pd.to_datetime(df.loc[c.index, col])
        df[col] = pd.to_datetime(df[col])
        return df

s='sem dinheiro'
company = 'sfra'
print('Antes do try')
try:
        passa = pd.read_pickle('passageiros e Pontos ida.zip', compression='zip')
        departures = pd.read_pickle('passagem por ponto %s.zip'%s, compression='zip')
        print()
except:
        departures = pd.read_pickle('passagem por ponto sem dinheiro.zip', compression='zip')
        departures = fix_date(departures, 'data_saida')
        departures = fix_date(departures, 'data_chegada')
        departures = fix_date(departures, 'HORA PARTIDA')
        departures = departures.sort_values('data_saida')
        departures = departures.dropna(subset=['data_saida',])
        print(departures.columns)
        print(departures)
        
        #departures['data_saida'] = pd.to_datetime(departures['data_saida'].astype(str))
        #print(departures.loc[b.index, 'data_saida'])
        #print(3)
        #departures = departures[departures['sentido']=='Volta']
        #departures['line_number'] = ''
        #departures['line_name'] = ''
        #departures[['line_number', 'line_name']] = departures['line'].str.split(' - ').to_list()
        departures['number_line'] = departures['number_line'].astype(int)
        departures.loc[departures['number_line'].astype(int) == 7151, 'number_line'] = 715
        
        #passa = pd.read_excel('ppp/movimento_linha_716_160519.xls', sheet_name=None)
        passa = pd.read_pickle('passageiros.zip', compression='zip')
        print(passa['SITUACAO'] == 'Ok')
        passa = passa[passa['SITUACAO'] == 'Ok']
        print(passa['SITUACAO'])
        
        passa = passa.loc[passa.LINHA.astype(int).isin([716]), :]
        
        try:
            passa['HORARIO'] = pd.to_datetime(passa['HORA'].astype(str), format='%d/%m/%Y %H:%M:%S', errors='coerce')
            passa['DATA'] = pd.to_datetime(passa['HORA'].astype(str).str.split(n=1, expand=True)[0], format='%d/%m/%Y', errors='coerce')
        except:
            passa['DATA'] = pd.to_datetime(passa['HORARIO'].astype(str).str.split(n=1, expand=True)[0], format='%d/%m/%Y', errors='coerce')
            passa['HORARIO'] = pd.to_datetime(passa['HORARIO'].astype(str), format='%d/%m/%Y %H:%M:%S', errors='coerce')
            
        
        print(passa['DATA'].unique())
        print(passa.head())
        #passa = [e for e in passa.values() if not e.empty]
        #print(passa)
        #passa = pd.concat(passa, ignore_index=True)
        #passa = passa[passa['LINHA']]
        linhas = sorted(list(set(passa['LINHA'].values)))
        passa = fix_date(passa, 'HORARIO')
        passa = fix_date(passa, 'DATA')


        #print(passa)
        
        carros_com_erro_DICT = {8563: 3563, 7331: 2114, 7371: 2118, 7029: 2902}
        passa.loc[:, 'CARRO'] = passa.loc[:, 'CARRO'].apply(lambda x: carros_com_erro_DICT.get(int(x), int(x)))

        for linha in linhas:
                print(linha)
                passa1 = passa.copy()
                passa1 = passa1[passa1['LINHA'].astype(int)==int(linha)]
                
                carros = set(passa1['CARRO'].values)
                print(carros)
                
                departures1 = departures.copy()
                departures1 = departures1[departures1['number_line'].astype(int)==int(linha)]
                print('Dep', departures1['car'].unique())
                #print('*********************')
                #print(passa1.head())
                #print('*********************')
                #print(departures1.head())
                carros_com_erro = []
                LOCAL_FROM_PASS = {}
                for carro in carros:
                        erro = False
                        achou_algum = False
                        
                        pas = passa1.copy()
                        pas = pas[pas['CARRO'].astype(int) == int(carro)]
                        
                        
                        if int(carro) in carros_com_erro_DICT:
                                carro = carros_com_erro_DICT[int(carro)]
                        #get Data from 
                        dep = departures1.copy()
                        dep  = dep[dep['car'].astype(str)==str(carro)].dropna(subset=['car',])
                        
                        dep = dep.sort_values(by=['data_saida'])

                        dep.index = pd.to_datetime(dep['data_saida'],  unit='s')
                        
                        dep = dep.loc[~dep.index.duplicated(keep='first')]
                        
                        if dep.empty:
                            continue
                        
                        if pas.empty:
                            continue
                            #print(carro, type(carro), '\n\b', pas['CARRO'])
                        i = 0
                        #print(dep['hora_prevista'])
                        #print(dep)
                        for cartao, horario, carro in zip(pas['CARTAO'].values, pas['HORARIO'].values, pas['CARRO'].values):
                                
                                #print(cartao, horario, carro)
                                
                                
                                i +=1
                                
                                try:
                                        l = dep.iloc[dep.index.get_loc(pd.to_datetime(horario), method='nearest', tolerance=pd.Timedelta('10Min'))]
                                        LOCAL_FROM_PASS[(cartao, pd.to_datetime(horario))] = {'linha': l['atendimento'], 'partida': l['hora_prevista'], 'direction': l['direction_geral'], 'stop': l['stop_id'], 'via': ''}
                                        achou_algum = True
                                except:
                                        carros_com_erro.append((str(carro), str(pd.to_datetime(horario).day)))

                                        erro = True
                        print(carro, 'Erro: ', erro, 'Achou algum:',achou_algum)
                

                passa1['station'] = np.vectorize(get_local_pass)(passa1['CARTAO'].values, passa1['HORARIO'].values)
                passa1['linha'] = np.vectorize(get_linha_pass)(passa1['CARTAO'].values, passa1['HORARIO'].values)
                passa1['partida'] = np.vectorize(get_partida_pass)(passa1['CARTAO'].values, passa1['HORARIO'].values)
                passa1['sentido'] = np.vectorize(get_sentido_pass)(passa1['CARTAO'].values, passa1['HORARIO'].values)
                
                passa1['via'] = ''
                passa1['via'] = np.vectorize(get_via_pass)(passa1['CARTAO'].values, passa1['HORARIO'].values)
                passa1[passa1['station'] == 'erro'].to_pickle('RESULTS\\passageiros com erro '+ str(linha) +'.zip', compression='zip')
                passa1[passa1['station'] == 'erro'].to_excel('RESULTS\\passageiros com erro '+ str(linha) +'.xlsx')
                passa1 = passa1[passa1['station'] != 'erro']
                passa1.to_pickle('RESULTS\\passageiros e Pontos sem erro '+ str(linha) +'.zip', compression='zip')
                passa1.to_excel('RESULTS\\passageiros '+ str(linha) +'.xlsx')
                
        print('*****************************\nCarros com erro:\n- ', '\n- '.join(list(set([' - '.join(e) for e in carros_com_erro]))), sep='')
        






        
        

print(passa)

print(passa)


#### FILTROS

BB = []

SL = [
        #CIMA:
        'Terminal Cleto Marques' ,  'PN180' ,  'PN181' ,  'PN18211' ,  'PN2911' ,  'PN2811' ,  'PN7622' ,  'Estrada Desembargador Carlos de Gusmão, 838-974 - Santa Lúcia, Maceió - AL, Brasil' ,  'PN98' ,  'PN99' ,  'PN100' ,  'PN101' ,  'PN592' ,  'PN113' ,  'PN102' ,  'PN103' ,  'PN104' ,  'PN105' ,  'PN106' ,  'PN578' ,  'PN197' ,  'PN1983' ,  'PN200e' ,  'PN2012',
        # REAL
        'Terminal Integrado' ,  'PN849' ,  'Conjunto' ,  'PN852' ,  'unit' ,  'PN855' ,  'PN856' ,  'PN1002' ,  'PN899', # AV. CACHOEIRA DO MEIRIM (TI até Pátio)
        'Avenida Belmiro Amorim, 1847-1915 - Santa Lúcia, Maceió - AL, Brasil',  'PN192',  'PN193',  'PN194',  'PN195',  'PN196',  'PP11' ,  'PN226' # BELMIRO AMORIM
        'Terminal S.Lyra' , 'PN16' ,  'PN124' ,  'PN125' ,  'PN123' ,  'PN122' ,  'PN21' ,  'PN22' ,  'PN23' ,  'PN117' ,  'PN24' ,  'PN25' ,  'PN1018' ,  'PP33' ,  'PP348' ,  'PN225', 'PP2233' ,  'PP33' ,  'PN466',# Salvador Lyra / Dub. Leão
        ]

CL = [
        'Terminal Integrado' ,  'PN849' ,  'Conjunto' ,  'PN852' ,  'unit' ,  'PN855' ,  'PN856' ,  'PN1002' ,  'PN899', # AV. CACHOEIRA DO MEIRIM (TI até Pátio)
        'PP49', 'Terminal Cleto Marques' ,  'PN180' ,  'PN181' ,  'PN31' ,  'PN32' ,  'PN33' ,  'PN34' ,  'PN35', 'PN29' ,  'PN30', #CLETO
        'Terminal S.Lyra' , 'PN16' ,  'PN124' ,  'PN125' ,  'PN123' ,  'PN122' ,  'PN21' ,  'PN22' ,  'PN23' ,  'PN117' ,  'PN24' ,  'PN25' ,  'PN1018' ,  'PP33' ,  'PP348' ,  'PN225', 'PP2233' ,  'PP33' ,  'PN466',# Salvador Lyra / Dub. Leão
        ]

EG = ['UFAL 3', 'P FOR', 'PN918', 'PN959', 'PN778.', 'PN690', 'PN994', 'PN987', 'PN697', 'PN920', 'E G 2', 'PN919', 'PNGF - 589', 'UFAL - 1', 'PP52', 'E G3', 'Terminal Eustáquio Gomes', 'UFAL..', 'E G 4', 'PN597', 'PN683', 'PN1336', 'PN50986788', 'PN993', 'PN688', 'Unnamed-Cidade Universitária', 'PN990', 'UFAL', 'PN991', 'PN7501', 'UFAL 1', 'PN958', 'PN691.', 'PN9221', 'PN5141', 'PN5131', 'PN956', 'PN983', 'PN732', 'PP10', 'PN921', 'PN984', 'PN738', 'FISC', 'PN692', 'caixa', 'PN723', 'PP9', 'PN992', 'PN741', 'PN521', 'UFAL.', 'PN923', 'PN725']

'''
mask_util = (pd.to_datetime(passa['DATA'].dt.date) >= pd.to_datetime('2019-05-20')) & (pd.to_datetime(passa['DATA'].dt.date) <= pd.to_datetime('2019-05-24'))
mask_dom = (pd.to_datetime(passa['DATA'].dt.date) >= pd.to_datetime('2019-05-19')) & (pd.to_datetime(passa['DATA'].dt.date) <= pd.to_datetime('2019-05-19'))
mask_sab = (pd.to_datetime(passa['DATA'].dt.date) >= pd.to_datetime('2019-05-25')) & (pd.to_datetime(passa['DATA'].dt.date) <= pd.to_datetime('2019-05-25'))
linhas_sl = [36, 37, 42, 704]
linhas_042 = [42,]
linhas_cm = [39, 602]




#### FIM FILTROS
#### > > > SELEçÃO DE FILTROS

linhas = linhas_sl
dias = mask_util
station_list = SL
group = pd.Grouper(freq='3H')

#### 
passa = passa[passa['LINHA'].astype(int).isin(linhas)]
passa = passa.loc[dias]
passa = passa[passa['station'].isin(station_list)]
'''

m = pd.read_excel('media por ponto.xlsx')
DIC_MEAN = {}
np.vectorize(lambda station, mean: DIC_MEAN.setdefault(station, mean))
m.index = m['stop_id']
passa.index = passa['HORARIO']
print(m)
D = []
departures.index = departures['data_saida']
departures['day'] = departures['data_saida'].dt.dayofweek
departures = departures[departures['day']==3]
for station in set(passa['station'].values):
        p = passa[passa['station']==station]
        mean = DIC_MEAN.get(station, '30')

        
        d = departures[departures['stop_id']==station]
        mean = '5'
        d = d.groupby(pd.Grouper(freq=mean+'min')).count()['car']
        #@d = d.max()


        g = p.groupby(pd.Grouper(freq=mean+'min')).count()['via']
        g = g[g!=0]
        print(station)
        D.append({'station': station, 'max': g.max(), 'mean': g.mean(), 'median': g.quantile(.5), '70p': g.quantile(.7), 'max_car': d.max(), 'max_car_hour': d.idxmax()})
print('terminou')

pd.DataFrame(D).to_excel('demanda ponto.xlsx')




#passa.groupby('station').count()['CARTAO'].to_excel('demanda ponto.xlsx')

COUNT = passa.groupby('CARTAO').count()['station'].to_dict(OrderedDict)
#print(COUNT)
def get_count(cartao):
        return COUNT[cartao]
passa['count'] = np.vectorize(get_count)(passa['CARTAO'].values)


passa_dup = passa.copy()
passa_dup = passa_dup[passa_dup['count']>1]
FROM_DICT = passa.groupby('CARTAO').first()['station'].to_dict(OrderedDict)
e = {key: value for key, value in list(passa.groupby('CARTAO'))}
#print(e)
TO_DICT = passa.groupby('CARTAO').last()['station'].to_dict(OrderedDict)


get_from = lambda cartao: FROM_DICT[cartao]
get_to = lambda cartao: TO_DICT[cartao]

passa_dup['from'] = np.vectorize(get_from)(passa_dup['CARTAO'].values)
passa_dup['to'] = np.vectorize(get_to)(passa_dup['CARTAO'].values)
passa_dup = passa_dup[passa_dup['from'] != passa_dup['to']]
passa_dup['relation'] = passa_dup['from'] + ' - ' + passa_dup['to']
print(passa_dup)
r = passa_dup.groupby('relation').count()['EMPRESA'].sort_values()
r.name = 'QUANTIDADE'
r.to_excel('res.xlsx')

#print(passa.groupby('station').count())
#print(departures)
#print(passa)

#r = passa.groupby('station').count()['EMPRESA']
r = passa.groupby(['linha', group]).count()
del r['HORARIO']
print(r)
r = r.reset_index()
print(r)
r['FAIXA'] = r.HORARIO.dt.time
r = r.groupby(['FAIXA', 'linha']).sum()['EMPRESA']
r.name = 'QUANTIDADE'
r.to_excel('res.xlsx')

erro
