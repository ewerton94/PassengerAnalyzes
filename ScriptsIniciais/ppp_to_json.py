import pandas as pd
from datetime import timedelta, datetime
from numpy import nan
import xlrd
from django.utils import timezone

from tkinter import filedialog
from tkinter import *
from os import listdir
import sys
import numpy as np
import json
from leg import legenda_contexto

import PySimpleGUI as sg


prefix = ''



#import googlemaps
def break_in_cars(df):
    days = np.split(df, np.where(df[0] == 'Prefixo :')[0])
    #days = [ev[~ev[0].isna()] for ev in days if not isinstance(ev, np.ndarray)]
    days = [ev for ev in days if not (ev.empty or ev.reset_index().loc[0, 0] is nan)]
    return days

def break_in_stops(df):
    days = np.split(df, np.where(df[0] == 'Ponto :')[0])
    #days = [ev[~ev[0].isna()] for ev in days if not isinstance(ev, np.ndarray)]
    days = [ev for ev in days if not (ev.empty or ev.reset_index().loc[0, 0] == 'Prefixo :')]
    return days


def break_in_departure(df, DEBUG=False):
    days = np.split(df, np.where(df['ordem_ponto'] == 1)[0])
    #days = [ev[~ev[0].isna()] for ev in days if not isinstance(ev, np.ndarray)]
    days = [ev for ev in days if not (ev.empty)]
    if days:
        if len(days) == 1:
            days[0]['departure'] = 1
            return days
        if DEBUG:
            print(*days[:3])
        old = days[:]
        days = []
        for i, day in enumerate(old):
            if day[day['ordem_ponto'] == 1].empty:
                novos = np.split(df, np.where(df['ordem_ponto'] == day['ordem_ponto'].min())[0])
                for novo in novos:
                    days.append(novo)
            else:
                days.append(day)
                
        days = days[1:len(days)]

    r = []
    for i, day in enumerate(days):
        
        day['departure'] = i + 1
        day['ordem_ponto2'] = day['ordem_ponto'] 
        r.append(day.groupby('ordem_ponto2').last())
    return r

def fix_date(df, col):
        df[col] = df[col].astype(object)
        a = df[col].apply(type)
        b = a[a==int]
        c = a[a!=int]
        
        df.loc[b.index, col] = pd.to_datetime(df.loc[b.index, col], unit='ns')
        df.loc[c.index, col] = pd.to_datetime(df.loc[c.index, col])
        df[col] = pd.to_datetime(df[col])
        return df
def reduce_memory(df):
    #print('\n\n\n\n\n\n***************************\nInicial')
    #print(df.info())
    df_float = df.select_dtypes(include=['float'])
    converted_float = df_float.apply(pd.to_numeric,downcast='float')
    gl_int = df.select_dtypes(include=['int'])
    converted_int = gl_int.apply(pd.to_numeric,downcast='unsigned')
    df[converted_int.columns] = converted_int
    df[converted_float.columns] = converted_float
    gl_obj = df.select_dtypes(include=['object'])
    converted_int = None
    converted_float = None
    converted_obj = pd.DataFrame()
    for col in gl_obj.columns:
        num_unique_values = len(gl_obj[col].unique())
        num_total_values = len(gl_obj[col])
        if num_unique_values / num_total_values < 0.5:
            converted_obj.loc[:,col] = gl_obj[col].astype('category')
        else:
            converted_obj.loc[:,col] = gl_obj[col]
    
    df[converted_obj.columns] = converted_obj
    #print('\nFinal')
    #print(df.info())
    return df
DIC_PP = {}
df_final = None
df_base = None
df_by_car=None
r = None
def create_json_ppp(files, df_row=None, df_first_work=None):
    global STOPS_DICT
    global df_final
    global df_base
    global df_by_car
    global r
    print('Aqui')
    if df_first_work is None:
        print('FIRST')
        N = len(files)
        df_final = {}
        print(N)
        #gmaps = googlemaps.Client(key='AIzaSyALMrzfk81yAHOGscwBgZpeTfsOKgxsAxg ')
        final = []
        if df_row is None:
            for ii, file_handle in enumerate(files):
                print("%.2f"%((ii/(N))*100))
                df = pd.read_excel(file_handle, header=None)
                company = df.loc[5, 1]
                line = df.loc[6, 1]
                server = df.loc[7, 1]
                sentido = df.loc[8, 1].lower()
                pontos = [p.strip() for p in df.loc[11, 1].split(' , ')]
                pontos[-1] = pontos[-1][:len(pontos[-1])-2]
                #print(df.iloc[20])
                DIC_PP[line.split(' - ')[0] + '&' +server + '&' + df.loc[8, 1]] = pontos
                STOPS_DICT[(int(line.split(' - ')[0]), server.replace(' IDA', ''), df.loc[8, 1].lower())] = pontos
                print(pontos)
                print(line, server)
                #print(df)
                df_line = []
                cars = break_in_cars(df)
                for df_car in cars:
                    #print(df_car)
                    car = df_car.reset_index().loc[0, 1]
                    stops = break_in_stops(df_car)
                    for df_stop in stops:
                        stop = df_stop.reset_index().loc[0, 1]
                        df_stop.columns = ['data_chegada', 'velocidade_chegada', 'data_saida', 'velocidade_saida',	'sentido',  'tempo_no_ponto', 'distância']

                        del df_stop['velocidade_chegada']
                        del df_stop['velocidade_saida']
                        del df_stop['distância']
                        #print(stop)
                        teste = stop.split(' - ')
                        #print(stop_id)
                        end = ' - '.join(teste[int(len(teste)/2):]).strip()
                        if end in pontos:
                            stop_id = end
                            ENI = pontos.index(end) + 1
                        else:
                            #print(stop_id)
                            try:
                                stop_id = teste[0].strip()
                                ENI = pontos.index(stop_id) + 1
                            except:
                                stop_id = teste[0].strip() + ' - ' + teste[1].strip()
                                ENI = pontos.index(stop_id) + 1
                        '''
                        stop_data = STOPS_DICT.get(' - '.join([stop_id, company]))
                        if not stop_data:
                            if stop_id in pontos:
                                adress = stop.replace(stop_id+' - ', '')
                            else:
                                for ponto in pontos:
                                    if ponto in stop:
                                        adress = ponto
                                        stop_id = ponto
                                        break

                            #geocode_result = gmaps.geocode(adress)
                            #at, lon = geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']
                            #latlon = "%.6f, %.6f"%(lat, lon)
                            stop_data = {
                                'adress': 'adress',
                                'latlon': 'latlon'
                            }
                            STOPS_DICT[' - '.join([stop_id, company])] = stop_data

                        '''
                        df_stop['company'] = company
                        df_stop['stop_id'] = str(stop_id)
                        df_stop['adress'] = ' - '.join(stop.split(' - ')[1:])
                        #df_stop['latlon'] = stop_data['latlon']
                        df_stop['car'] = str(car)
                        df_stop['line'] = line
                        df_stop['atendimento'] = server.replace(' IDA', '')
                        n = ENI
                        df_stop['ordem_ponto'] = n
                        df_stop = df_stop.reset_index().iloc[4:]
                        
                        df_stop['data_chegada'] = pd.to_datetime(df_stop['data_chegada'], errors='coerce')
                        df_stop['data_saida'] = pd.to_datetime(df_stop['data_saida'], errors='coerce')

                        df_line.append(df_stop)
                df_stop = None
                df_line = pd.concat(df_line, ignore_index=True)
                
                print(df_line.head())
                df_line = reduce_memory(df_line)  
                final.append(df_line)     
                
            df_stop = []
            cars = []
            car = []
            df_car = []
            df = []
            df_final = pd.concat(final, ignore_index=True)
            print('Criando Partidas brutas')
            #df_final.to_excel('df_departures_row.xlsx')
            #print(df_final.info())
            #df_final = reduce_memory(df_final)
            #print(df_final.info())
            #df_final.to_csv('aa.csv')
            df_final.to_pickle('../Resultados/'+legenda_contexto+'/df_departures_row'+ prefix + '.zip', compression='zip')
            df_stops = pd.DataFrame(STOPS_DICT.values(), index =STOPS_DICT.keys())
            df_stops.to_pickle('../Resultados/'+legenda_contexto+'/stops '+ prefix + '.zip', compression='zip')
            print('\bCriado Partidas brutas')
        else:
            df_final = df_row
            df_stops = pd.read_pickle('../Resultados/'+legenda_contexto+'/stops '+ prefix + '.zip', compression='zip')
            df_stops['LISTA'] = df_stops.apply(list, axis=1)
            STOPS_DICT = df_stops['LISTA'].to_dict()
            for key in STOPS_DICT:
                STOPS_DICT[key] = [e for e in STOPS_DICT[key] if not e is None ]
            
        
        DICT_DP = {}
        print('Iniciou')
        df_final = df_final.copy().drop_duplicates(subset=['data_chegada', 'car', 'line'])
        #print(df_final.columns)
        
        #df_final = df_final[df_final['line'].str.startswith('4006')]
        #df_base = df_base[df_base['number_line']=='4006']
        df_final['max_ponto'] =  df_final.groupby('atendimento')['ordem_ponto'].transform(np.max)
        np.vectorize(lambda car, number_line, line, atendimento, direction, start, final, departure, ciclo: DICT_DP.setdefault(car, []).append((
            number_line, line, atendimento, direction, pd.to_datetime(start), pd.to_datetime(final), pd.to_datetime(departure), ciclo)))(
            df_base['car_number'].values,
            df_base['number_line'].values,
            df_base['name_line'].values,
            df_base['atendimento'].values,
            df_base['direction'].values,
            df_base['fulfilled_date_time'].values,
            df_base['final_date_time'].values,
            df_base['expected_date_time'].values,
            df_base['fulfilled_duration_total'].values,
            )
        new_dfs = []
        df_base= None
        #print(df_final['line'].str.split(' - ').to_list())
        #print(df_final['line'])
        #print(df_final['line'].unique())
        #print(df_final['line'].str.split(' - ', expand = True))
        df_nome_linha = df_final['line'].str.split(' - ', expand = True)
        try:
            df_nome_linha.loc[~df_nome_linha[2].isna(), 1] = df_nome_linha.loc[~df_nome_linha[2].isna(), 1].astype(str) + ' - ' + df_nome_linha.loc[~df_nome_linha[2].isna(), 2].astype(str)
        except:
            df_nome_linha[2] = np.nan
            df_nome_linha.loc[~df_nome_linha[2].isna(), 1] = df_nome_linha.loc[~df_nome_linha[2].isna(), 1].astype(str) + ' - ' + df_nome_linha.loc[~df_nome_linha[2].isna(), 2].astype(str)
        df_final[['number_line', 'line']] = df_nome_linha[[0, 1]]
        df_nome_linha = None
        #print(df_final)

        print('Percorrendo')
        total_ = len(list(DICT_DP.keys()))
        P = []
        j = 0
        #print(STOPS_DICT)
        COUNT_MASTER = 0
        for car in DICT_DP.keys():
            j += 1
            i = 1
            print()
            print('%.2f%%'%(100*j/total_))
            df_final_by_car = df_final[df_final['car'].astype(int)==int(car)]
            for departure in DICT_DP[car]:
                #print(df_final.columns)
                df_by_car = df_final_by_car[(df_final_by_car['sentido'].str.lower() == departure[3]) & (df_final_by_car['number_line'].astype(int)==int(departure[0]))].copy()
                
                #print(df_by_car)
                df2 = df_by_car[['ordem_ponto', 'stop_id']].drop_duplicates(subset=['ordem_ponto']).sort_values('ordem_ponto')
                try:
                    filtro_pontos = STOPS_DICT[(int(departure[0]), departure[2], departure[3].lower())]
                except:
                    print("ERRO", (int(departure[0]), departure[2], departure[3].lower()))
                    continue
                df2 = df2[df2['stop_id'].isin(filtro_pontos)]
                index = [i for i in range(1, len(filtro_pontos)+1)]#df2['ordem_ponto'].values
                #index = [i for i in range(1, len(filtro_pontos)+1)]#df2['ordem_ponto'].values
                stop_id = filtro_pontos#df2['stop_id'].values
                
                #print('index')
                #print(index)

                if df_by_car.empty:
                    print('\n\nERRO no começo\n\n')
                    print(car)
                    P.append(car)
                    continue
                c = df_by_car.loc[df_by_car.index[0], 'company']
                df_by_car['data_saida'] = pd.to_datetime(df_by_car['data_saida'], errors='coerce')
                df_by_car['data_chegada'] = pd.to_datetime(df_by_car['data_chegada'], errors='coerce')
                df_by_car = df_by_car.dropna(subset=['data_saida', 'data_chegada'])
                
                mask = (df_by_car['data_saida'] >= pd.to_datetime(departure[4])) & (df_by_car['data_chegada'] <= pd.to_datetime(departure[5]))

                r = df_by_car.copy().loc[mask]
                if r.empty:
                    r = df_by_car.copy()
                #else:
                #    print(r)
                    
                #print('\n\nR MASCARADO\n\n')
                #print(r)
                r['n_departure'] = i
                
                
                
                r = r.sort_values(by=['data_saida'])
                #print('\n\n\nORDENADOOO: \n')
                #print(r)
                r['delta_order'] = r['ordem_ponto'].diff(-1)
                r['delta_order_2'] = r['ordem_ponto'].diff(1)
                r['ordem_ponto2'] = r['ordem_ponto']
                r['departure2'] = r['n_departure']
                r = r[(r['delta_order']<0) | (r['delta_order_2'] <0) | (r['delta_order_2'] == 1)]

                r['delta_order'] = r['ordem_ponto'].diff(1)
                r = r[(r['ordem_ponto'] == 1) | (r['delta_order'] >0)]
                r = r.groupby(['ordem_ponto2', 'departure2']).last()
                if r.empty:
                    print(df_by_car.head())
                    
                    continue
                r.set_index('ordem_ponto', inplace=True)
                r = r.reindex(index)
                r2 = r.dropna(subset=['atendimento']).reset_index()
                

                try:
                    if not r2.empty:
                    
                        
                        if pd.isnull(r.loc[r.index[0], 'index']):
                            r.loc[r.index[0], :] = r2.loc[0, :]
                            r.loc[r.index[0], 'data_saida'] = departure[4]
                            r.loc[r.index[0], 'data_chegada'] = departure[4]
                        if pd.isnull(r.loc[r.index[-1], 'index']):
                            r.loc[index[-1], :] = r2.loc[r2.index[-1], :]
                            r.loc[index[-1], 'data_saida'] = departure[5]
                            r.loc[index[-1], 'data_chegada'] = departure[5]
                    
                    if pd.isnull(r.loc[1, 'data_saida']):
                        r_base = r.dropna(subset=['atendimento']).reset_index()
                        r.loc[1, :] = r_base.loc[0, :]
                        r.loc[1, ['data_saida', 'data_chegada']] = departure[4]
                    if pd.isnull(r.loc[r.index[-1], 'data_saida']):
                        r_base = r.dropna(subset=['atendimento']).reset_index()
                        r.loc[index[-1], :] = r_base.loc[0, :]
                        r.loc[index[-1], ['data_saida', 'data_chegada']] = departure[5]
                        
                        
                    r['atendimento'] = departure[2]
                    r['direction_geral'] = departure[3]
                    day = pd.to_datetime(departure[6]).date()
                    r['DATAA'] = day
                    r['HORA PARTIDA'] = departure[4]
                    r['hora_prevista'] = departure[6]
                    r['duracao_ciclo'] = departure[7]
                
                    
                    

                        
                        
                    
                    r = r.interpolate(method='ffill')
                    
                    r2 = r.select_dtypes(include=['datetime'])
                    for col in r2:
                        r2[col] = r2[col].dt.hour*60*60 + r2[col].dt.minute*60 + r2[col].dt.second
                        #r2[col] = r2[col].dt.days*24*60*60 + r2[col].dt.seconds
                    #print(r2)
                    #r2 = r2.dt.days*24*60*60 + r2.dt.seconds
                    #r2 = r2.apply(pd.to_numeric, downcast='float')
                    if True:#try:
                        r2[r2<0] = np.nan
                        
                        r2 = r2.interpolate(method='linear')
                        #print(r2)
                        day  =pd.to_datetime(day)
                        for col in r2:
                            r2[col] = r2[col].apply(lambda x: pd.Timedelta(seconds=x) + day)
                        #r2 = r2.apply(pd.to_datetime, unit='ns')
                        #print(r2)
                        #dddd
                        r[r2.columns] = r2
                        
                        r['number_line'] = departure[0]
                        r['name_line'] =  departure[1]
                        r['company'] =  c
                        r = r.fillna(method='ffill')
                        r = r.reset_index()
                        r['hora_prevista'] = departure[6]
                        
                        r = r[['ordem_ponto', 'DATAA', 'HORA PARTIDA','hora_prevista', 'atendimento', 'data_chegada', 'data_saida', 'direction_geral', 'n_departure', 'company', 'number_line', 'name_line', 'duracao_ciclo']]
                        r['stop_id'] = stop_id
                        r['car'] = car
                        
                        #print(r)
                        #print(r[['ordem_ponto', 'data_chegada', 'data_saida']])
                        #roooooo
                        
                        new_dfs.append(reduce_memory(r.copy()))
                        COUNT_MASTER += 1


                        i +=1
                except:
                    print('Erro')
                #except:
                #    print('ERRO - Complexo')
                #    print(r)
                #    print(r.head())

                
        print('Criando Passagem por ponto com base no tempo de viagem')
        
        try:
            df_final = pd.concat(new_dfs, ignore_index=True)
            #print(df_final)
        
            #df_final.to_excel('df_departures_first.xlsx')
            df_final.to_pickle('../Resultados/'+legenda_contexto+'/passagem por ponto'+ prefix + '.zip', compression='zip')
            df_final.to_excel('passagem por ponto'+ prefix + '.xlsx')
            print('Criado Passagem por ponto com base no tempo de viagem')
        except:
            print('Deu erro, separando em 4 arquivos')
            df_final = pd.concat(new_dfs[:int(COUNT_MASTER/4)], ignore_index=True)
        
            #df_final.to_excel('df_departures_first.xlsx')
            df_final.to_pickle('../Resultados/'+legenda_contexto+'/passagem por ponto'+ prefix + ' 1.zip', compression='zip')
            print('1 foi')
            df_final = pd.concat(new_dfs[int(COUNT_MASTER/4): int(COUNT_MASTER/2)], ignore_index=True)
            
        
            #df_final.to_excel('df_departures_first.xlsx')
            df_final.to_pickle('../Resultados/'+legenda_contexto+'/passagem por ponto'+ prefix + ' 2.zip', compression='zip')
            print('2 foi')

            df_final = pd.concat(new_dfs[int(COUNT_MASTER/2):int(COUNT_MASTER/2) + int(COUNT_MASTER/4)], ignore_index=True)
        
            #df_final.to_excel('df_departures_first.xlsx')
            df_final.to_pickle('../Resultados/'+legenda_contexto+'/passagem por ponto'+ prefix + ' 3.zip', compression='zip')
            print('3 foi')

            df_final = pd.concat(new_dfs[int(COUNT_MASTER/2) + int(COUNT_MASTER/4):], ignore_index=True)
        
            #df_final.to_excel('df_departures_first.xlsx')
            df_final.to_pickle('../Resultados/'+legenda_contexto+'/passagem por ponto'+ prefix + ' 4.zip', compression='zip')
            print('4 foi')

    else:
        df_final = df_first_work
    
    df_final = df_final.sort_values(by=['data_saida'])
    df_final['stop_id2'] = df_final['stop_id']
    df_final['departure'] = df_final['n_departure']
    df_final['car2'] = df_final['car']
    df_final['sentido2'] = df_final['direction_geral']

    df_final = df_final.groupby(['stop_id', 'departure', 'car2', 'sentido2']).last().reset_index()

    df_final = df_final.sort_values(by=['car', 'n_departure','data_chegada'])
    print('Criando passagem por ponto')


    df_final.to_pickle('../Resultados/'+legenda_contexto+'/passagem por ponto final'+ prefix + '.zip', compression='zip')
    #df_final.to_excel('passagem por ponto.xlsx')
    
    #print(df_final.head())
    print('Criado passagem por ponto')
    '''
    dfs = []
    for atendimento, df_at in df_final.groupby('atendimento'):
        
        for car, df_car in df_at.groupby('car'):
            for sentido, df in df_car.groupby('sentido'):
                df = df.sort_values(by=['data_saida'])
                #if sentido == 'Ida':
                df['delta_order'] = df['ordem_ponto'].diff(-1)
                df['delta_order_2'] = df['ordem_ponto'].diff(1)
                df['delta_time'] = pd.to_datetime(df['data_chegada']).diff(1)
                #if int(car) == 3217:
                #    print(df)

                if df.empty:
                    print('ERROO\n\n\n\n\n-------------------------------\n\n\n\n')
                    print(df)
                else:
                    deps = break_in_departure(df, int(car) == 2617)
                    if not deps:
                        print('ERROO\n\n\n\n\n-------------------------------\n\n\n\n')
                        print(car)
                        print(df)
                        print(list(set(df['departure'].values)))
                        print(deps)
                    else:
                        df = pd.concat(deps, ignore_index=True)
                        #if int(car) == 3217:
                        #    #print(df)
                        #    print(deps)
                        #print(df)
                        #print('0-----')
                        df['ordem_ponto2'] = df['ordem_ponto']
                        df['departure2'] = df['departure']
                        df = df[(df['delta_order']<0) | (df['delta_order_2'] <0) | (df['delta_order_2'] == 1)]
                        df['delta_order'] = df['ordem_ponto'].diff(1)
                        df = df[(df['ordem_ponto'] == 1) | (df['delta_order'] >0)]
                        df = df.groupby(['ordem_ponto2', 'departure2']).last()
                        #print(df)
                        
                        #print(df[['sentido', 'data_chegada', 'data_saida', 'ordem_ponto', 'delta_order', 'stop_id', 'car']])
                        #df = df[df['delta_order']<0]
                        #df['delta_order'] = df['ordem_ponto'].diff(1)
                        #print(df[['sentido', 'data_chegada', 'data_saida', 'ordem_ponto', 'delta_order', 'stop_id', 'car']])
                        #print(df[['sentido', 'data_chegada', 'data_saida', 'ordem_ponto', 'delta_order', 'stop_id', 'car']])
                        #df = df.loc[df[(df['ordem_ponto'] == 1)].index[0]:, :]
                        #df = df.reset_index()
                        #df = df.loc[:df[(df['ordem_ponto'] == 1)].index[-1]-1, :]
                        ''    
                        else:
                            

                            #print('____________________')
                            #print(df_car)
                            df['delta_order'] = df['ordem_ponto'].diff(1)
                            #print(df[['sentido', 'data_chegada', 'data_saida', 'ordem_ponto', 'delta_order', 'stop_id', 'car']])
                            
                            #print('____________________')
                            df = df[df['delta_order']>0]
                            #df['delta_order'] = df['ordem_ponto'].diff(1)
                            
                            
                            #df = df[df['delta_order']>0]
                        ''

                        dfs.append(df)
            

    df_final = pd.concat(dfs, ignore_index=True)
    df_final['stop_id2'] = df_final['stop_id']
    df_final['departure2'] = df_final['departure']
    df_final['car2'] = df_final['car']
    df_final['sentido2'] = df_final['sentido']

    df_final = df_final.groupby(['stop_id', 'departure2', 'car2', 'sentido2']).last().reset_index()

    df_final = df_final.sort_values(by=['car', 'departure','data_chegada'])
    del df_final['delta_order']
    del df_final['delta_order_2']
    del df_final['delta_time']
    df_final.to_pickle('../Resultados/'+legenda_contexto+'/passagem por ponto.zip', compression='zip')
    df_final.to_excel('passagem por ponto.xlsx')
    '''
    return ''

#sg.ChangeLookAndFeel('GreenTan')

dp_geral = pd.read_pickle('../Resultados/'+legenda_contexto+'/departures total'+ prefix + '.zip', compression='zip')

dp_errors = dp_geral[dp_geral['fulfilled_duration'].isna()]
dp_geral = dp_geral[~dp_geral['fulfilled_duration'].isna()]
dp_geral = dp_geral[~dp_geral['expected_date_time'].isna()]
dp_geral = dp_geral[~dp_geral['fulfilled_date_time'].isna()]
print(dp_geral['fulfilled_date_time'])
print(dp_geral['expected_date_time'])




try:
    df_row = pd.read_pickle('../Resultados/'+legenda_contexto+'/df_departures_row'+ prefix + '.zip', compression='zip')
    files = []
except:
    df_row = None
    df_departures_first = None

    '''
    form = sg.FlexForm('Everything bagel', default_element_size=(40, 1))

    layout = [
        [sg.Text('Selecione a pasta com os arquivos do GoolSystem: ', size=(40, 1), auto_size_text=False, justification='right'),
        sg.InputText('Default Folder'), sg.FolderBrowse()],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window(
        'Passageiros para json',
        layout=layout,
        default_element_size=(12,1),
        font='Helvetica 18',
    )
    event, values = window.Read()
    '''
    folder_selected = '../ArquivosEntrada/'+legenda_contexto+'/TPP'
    #root = Tk()
    #root.withdraw()
    #folder_selected = filedialog.askdirectory()
    print('\n\nPasta selecionada!\n\nVocê selecionou a pasta:', folder_selected,'\n\n')
    #print(listdir(folder_selected))

    files = [folder_selected + '/' + f for f in listdir(folder_selected) if f.startswith('TempoPermanenciaPonto')]




try:
    df_departures_first = pd.read_pickle('../Resultados/'+legenda_contexto+'/df_departures_first'+ prefix + '.zip', compression='zip')
    files = None
except:
    df_departures_first = None



dp_geral['final_date_time'] = dp_geral['fulfilled_date_time'] + np.vectorize(np.timedelta64)(dp_geral['fulfilled_duration'].astype(int).values, 'm')


dp_geral = fix_date(dp_geral, 'final_date_time')
dp_geral = fix_date(dp_geral, 'fulfilled_date_time')
dp_geral = fix_date(dp_geral, 'expected_date_time')
#dp_geral = dp_geral.sort_values('data_saida')#print(list(zip(dp_geral['fulfilled_date_time'].values, dp_geral['final_date_time'].values))[:5])
#print(dp_geral)
#print(dp_errors)


with open('../Resultados/'+legenda_contexto+'/STOPS.json') as json_data:
    STOPS_DICT = json.load(json_data)
    
dp_geral.reset_index(inplace=True)
df_base=dp_geral
dp_geral = None
create_json_ppp(files, df_row, df_departures_first)
#print(STOPS_DICT)
with open('../Resultados/'+legenda_contexto+'/stops_by_line.json', 'w') as json_data:
    json.dump(DIC_PP, json_data)

print('\n\n\n\n\n\n\n\n\n\n>>>>>>>>>>>>>>>\n\nFinalizado Tempo por Ponto')

#df = pd.read_json('departures.json')
#print(df[df['fulfilled_duration'].isna()])
