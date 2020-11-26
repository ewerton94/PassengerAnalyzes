# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


df = pd.read_pickle('PONTOS LOC.zip', compression='zip')


df.loc[df['latlon']=='None', 'latlon'] = np.nan


df[['LAT', 'LON']] = df['latlon'].str.split(',', expand=True)
df['LAT'] = df['LAT'].astype(float)
df['LON'] = df['LON'].astype(float)
df['LON'] = df['LON'].fillna(method='bfill')
df['LAT'] = df['LAT'].fillna(method='bfill')
df['latlon'] = df['LAT'].astype(str) + ', ' + df['LON'].astype(str)
df.groupby('latlon').first().to_excel('pontos_todos com correcao.xlsx')

df.drop(['LAT', 'LON'], axis=1, inplace=True)


por_endereco = pd.read_excel('pontos corrigidos.xlsx').groupby('adress').agg('first')
por_endereco = por_endereco.to_dict('index')

df.loc[:, 'latlon'] = np.vectorize(lambda x, y: por_endereco.get(x, {'latlon': y})['latlon'])(df['adress'].values, df['latlon'].values)

terminais = pd.read_excel('Terminais.xlsx').groupby(['company', 'code']).agg('first')
terminais = terminais.to_dict('index')
df.loc[:, 'terminal'] = np.vectorize(lambda x, y: terminais.get((x, y), {'terminal': ''})['terminal'])(df['company'].values, df['stop_id'].values)

df['linha'] = df['line'].str.split(' - ', expand=True)[0].astype(int)

df[['linha', 'stop_id', 'latlon','terminal']].to_pickle('Base de dados - pontos.zip', compression='zip')
df.groupby('latlon').first().to_excel('pontos_todos.xlsx')
