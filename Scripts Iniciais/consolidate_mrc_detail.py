# -*- coding: utf-8 -*-
import pandas as pd
import os
dfs = []
for file in os.listdir('files'):
    if file.endswith('.zip'):
        df = pd.read_pickle('files/'+file, compression='zip')
        df.columns = ['HORARIO', 'CARTAO', 'TIPO', 'SITUACAO', 'SENTIDO', 'LINHA', 'VALOR', 'EMPRESA',
       'CARRO', 'MOTORISTA', 'COBRADOR']
        #df.to_excel(file+'.xlsx')
        dfs.append(df)

df = pd.concat(dfs, ignore_index=True)
df.to_pickle('passageiros 035 25 ago.zip', compression='zip')
