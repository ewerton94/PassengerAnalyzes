from io import StringIO
import numpy as np
import os
import pandas as pd
import threading
#from core.models import Car, Line, Company, SourceCar, Manufacturer, Model, Chassis, Bodyworker, Engine
from unicodedata import normalize
from datetime import datetime
from leg import legenda_contexto
#from operation.models import PassengerByCardType
def break_at_text(df, condition): 
    brokens = np.split(df, condition[0])
    brokens = [ev.reset_index(drop=True) for ev in brokens if not (ev.empty or ev['hora'].count()<=2)]
    return brokens
def read_file(file):
    with open(file, 'r', encoding="latin-1") as FILE:
        cols = ['hora','cartao','tipo','situacao',4,'sentido',6,'linha','valor',9]
        texto = normalize('NFKD', FILE.read()).encode('utf-8', 'ignore').decode('utf-8').replace(',', '.').replace('TOTAL:', 'TOTAL:;').replace('TOTAL GERAL:', 'TOTAL GERAL:;').replace('DATA FINAL UTILIZAÇÃO: ', ';DATA FINAL UTILIZAÇÃO:;').replace('DATA INICIAL UTILIZAÇÃO: ', ';DATA INICIAL UTILIZAÇÃO: ;').replace('DATA INICIAL PROCESSAMENTO:',';DATA INICIAL PROCESSAMENTO:')
        df = pd.read_csv(StringIO(texto), sep=';', header=None, names=cols, skiprows=1)
        df = df[['hora', 'cartao', 'tipo', 'situacao', 'sentido','linha','valor']]
        companies = break_at_text(df, np.where(df['hora'] == 'TOTAL EMPRESA:'))
        
        final = []
        for company in companies:
            company['Empresa'] = company.loc[1, 'hora']
            cars = break_at_text(company, np.where(company['hora'] == 'Carro:'))
            for car in cars:
                car['carro'] = car.loc[0, 'cartao']
                car['motorista'] = car.loc[0, 'situacao']
                car['cobrador'] = car.loc[0, 'sentido']
                car = car[~car.valor.isna()]
                car = car[car['hora']!='Carro:']
                final.append(car)
        df = pd.concat(final, ignore_index=True)
        df.to_pickle(file + '.zip', compression='zip')
        print('finalizado ', file)
        
class ReadThread(threading.Thread):
    def __init__(self, file=None):
        self.file = file
        
        threading.Thread.__init__(self)

    def run (self):
        read_file(self.file)
        
        
for file in os.listdir('../ArquivosEntrada/'+legenda_contexto+'/RC'):
    ReadThread('../ArquivosEntrada/'+legenda_contexto+'/RC/'+file).start()