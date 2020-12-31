from leg import legenda_contexto
import os
import pandas as pd
import numpy as np

pre = '../Resultados/'+legenda_contexto+'/'
pos = ''

arquivos = [pre + 'PassageirosPorPonto/'+f for f in os.listdir(pre + 'PassageirosPorPonto/') if f.endswith('.zip')]
dfs = []
for a in arquivos:
    df = pd.read_pickle(a, compression='zip')
    dfs.append(df)
df = pd.concat(dfs, ignore_index=True)

print(df)

df = df.dropna(subset=['partida'])

print(df)

df = df[df.station.isin(['PN974', 'PN627'])]

df2 = df.groupby(['LINHA', 'partida']).count()['HORARIO'].reset_index()
print(df2)
df2['partida2'] = df2['partida'].dt.time
for linha in df2.LINHA.unique():
    df3 = df2[df2.LINHA == linha]
    df3 = df3.groupby(['LINHA','partida2']).mean().reset_index()
    df4 = pd.pivot_table(df3, values='HORARIO', index=[ 'partida2'],
                        columns=['LINHA'])
    df4.to_excel(linha + '.xlsx')


print(df)