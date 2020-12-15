import pandas as pd
import numpy as np
from .models import *

DIAS = ['Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado', 'Domingo']
DIAS_ORDEM = ['Domingo', 'Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado']

class BaseData():
    columns = []
    def __init__(self, queryset):
        self.queryset = queryset
        self.df = self.get_df()

    def get_df(self):
        self.df = pd.DataFrame(list(self.queryset.values_list(*self.columns)), columns=self.columns)
        return self.df

class DadosResumo(BaseData):
    columns = ['id', 'partida_id']
class DadosPorDiaDaSemana(BaseData):
    
    columns = ['id', 'horario']

    def calcular(self):
        df = self.get_df()
        print(df)
        df['Dia da Semana'] = pd.to_datetime(df['horario']).dt.dayofweek.apply(lambda x: DIAS[x])
        df = df.groupby('Dia da Semana').count()
        df = df[['id',]]
        df.columns = ['Passageiros']
        df = self.ordenar_index(df, lambda x: DIAS_ORDEM.index(x))

        print(df)
        return self.grafico_de_barras(df)

        print(df)
    def ordenar_index(self, df, key):
        df['sort_param'] = np.vectorize(key)(df.index)
        return df.sort_values('sort_param').drop('sort_param', 1)

    def grafico_de_barras(self, df):
        xaxis = df.index
        series = []
        for col in df.columns:
            series.append({
                'name': col,
                'data': df[col].values
            })
        return {
            'xaxis': {
                'categories': xaxis
            },
            'series': series
        } 
        

    



