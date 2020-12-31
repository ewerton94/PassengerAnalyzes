# -*- coding: utf-8 -*-
import pandas as pd
import os
from leg import legenda_contexto
dfs = []
for file in os.listdir('../ArquivosEntrada/'+legenda_contexto+'/RC'):
    if file.endswith('.zip'):
        df = pd.read_pickle('../ArquivosEntrada/'+legenda_contexto+'/RC/'+file, compression='zip')
        df.columns = ['HORARIO', 'CARTAO', 'TIPO', 'SITUACAO', 'SENTIDO', 'LINHA', 'VALOR', 'EMPRESA',
       'CARRO', 'MOTORISTA', 'COBRADOR']
        #df.to_excel(file+'.xlsx')
        dfs.append(df)

df = pd.concat(dfs, ignore_index=True)
df.to_pickle('../Resultados/'+legenda_contexto+'/passageiros.zip', compression='zip')
