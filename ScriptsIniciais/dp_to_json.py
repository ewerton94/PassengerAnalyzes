import pandas as pd
from datetime import timedelta, datetime
from numpy import nan
import xlrd
from django.utils import timezone

from tkinter import filedialog
from tkinter import *
from os import listdir
import sys
from leg import legenda_contexto



def create_json_departures(files, III):
    N = len(files)
    df_final = {}
    unique = 0
    for ii, file_handle in enumerate(files):
        print("%.2f"%((ii/(N))*100))
        try:
            df = pd.read_excel(file_handle, header=None)
            number_line, name_line = df.loc[3, 16].split(' - ')
            company_name = df.loc[3, 7]
            print('\n#### ', company_name, ' ####')
            print('##   ', name_line, '   ##')
            date = df.loc[3, 2]
            header = 11
            new_header = pd.io.parsers.ParserBase({'names':df.iloc[header]})._maybe_dedup_names(df.iloc[header]) #grab the first row for the header
            df = df[header + 1:] #take the data less the header row
            df.columns = new_header #set the header row as the df header
            #departures = df[df['Sentido'] == 'Ida']
            departures = df.dropna(subset=['Posição',])
            if True:
                #company = Company.objects.get(name=company_name)
                if int(number_line) in list(range(1000, 1030)) and 'eleiro' in company_name:
                    continue
                #meta_line, _ = MetaLine.objects.get_or_create(name=name_line, number=number_line, company=company)
                i = 0


                for index, row in departures.iterrows():
                    unique += 1
                    try:
                        sentido = row['Sentido'].lower()
                        atendimento = row['Atendimento'].replace(' IDA', '')
                        #line, _ = Line.objects.get_or_create(meta_line=meta_line, atendimento=atendimento)
                        #print(date)
                        #print(row['Prev.'], row['Real.'])
                        if isinstance(row['Prefixo'], str):
                            car_number = int(row['Prefixo'].split(' - ')[0])
                        elif isinstance(row['Prefixo'], int):
                            car_number = int(row['Prefixo'])
                        else:
                            print('Problema com veículo ', row['Prefixo'], 'da linha ', atendimento)
                            print(file_handle)
                            #input('Digite enter...')
                            continue
                        #car = Car.objects.filter(number=car_number)
                        #if car:
                        #    car = car[0]
                        #else:
                        #    print('Problema com veículo ', row['Prefixo'], 'da linha ', line)
                        #    continue

                        i += 1

                        #IDA
                        try:
                            expected_date_time = datetime.strptime(' '.join([date, row['Prev.']]), '%d/%m/%Y %H:%M')
                            expected_date_time = None if expected_date_time is nan else expected_date_time
                        except:
                            expected_date_time = None
                        try:
                            fulfilled_date_time =  datetime.strptime(' '.join([date, row['Real.']]), '%d/%m/%Y %H:%M')
                            fulfilled_date_time = None if fulfilled_date_time is nan else fulfilled_date_time
                        except:
                            fulfilled_date_time = None
                        try:
                            expected_duration = row['Prev..2']
                            expected_duration = None if expected_duration is nan else expected_duration
                        except:
                            expected_duration = None
                        try:
                            fulfilled_duration = row['Real..2']
                            fulfilled_duration = None if fulfilled_duration is nan else fulfilled_duration
                        except:
                            fulfilled_duration = None
                            
                        try:
                            fulfilled_duration_total =  int(row['Real..3'])
                            fulfilled_duration_total = None if fulfilled_duration_total is nan else fulfilled_duration_total
                        except:
                            fulfilled_duration_total = None
                        
                        pos = row['Posição']
                        if not pos:
                            pos = 1
                        
                        df_final.setdefault('row', []).append(unique)
                        df_final.setdefault('order', []).append(pos)
                        df_final.setdefault('fulfilled_duration_total', []).append(fulfilled_duration_total)

                        
                        
                        df_final.setdefault('name_line', []).append(name_line)
                        df_final.setdefault('atendimento', []).append(atendimento)
                        df_final.setdefault('company_name', []).append(company_name)
                        df_final.setdefault('car_number', []).append(car_number)
                        df_final.setdefault('number_line', []).append(number_line)
                        df_final.setdefault('expected_date_time', []).append(expected_date_time)
                        df_final.setdefault('fulfilled_date_time', []).append(fulfilled_date_time)
                        df_final.setdefault('expected_duration', []).append(expected_duration)
                        df_final.setdefault('fulfilled_duration', []).append(fulfilled_duration)
                        df_final.setdefault('direction', []).append(sentido)

                            

                    except:
                        print('ERRRR')
                        print(company, meta_line)
                        print(row)
        except:
            pass
    for key in df_final:
        print(key, '-', len(df_final[key]))
    df = pd.DataFrame(df_final)
    #df.to_pickle('departures%s.zip'%III, compression='zip')
    return df
    #df.to_json('departures%s.json'%III)



    return 'Partidas cadastradas com sucesso.'



folder_selected = '../ArquivosEntrada/'+legenda_contexto+'/TV'

print(listdir(folder_selected))
final = []
for folder in listdir(folder_selected):
    if folder.endswith('.md'):
        continue
    files = [folder_selected  + '/' + folder + '/' + f for f in listdir(folder_selected  + '/' + folder) if f.startswith('TempoViagem')]
    df = create_json_departures(files, ' - ' + folder)
    print(df)
    final.append(df)
    print('\n\n\n\n\n\n\n\n\n\n>>>>>>>>>>>>>>>')
final = pd.concat(final, ignore_index=True)
final.to_pickle('../Resultados/'+legenda_contexto+'/departures total.zip', compression='zip')
#final.to_excel('departures total.xlsx')

