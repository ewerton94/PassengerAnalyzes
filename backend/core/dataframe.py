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
        df['Dia da Semana'] = pd.to_datetime(df['horario']).dt.dayofweek.apply(lambda x: DIAS[x])
        df = df.groupby('Dia da Semana').count()
        df = df[['id',]]
        df.columns = ['Passageiros']
        df = self.ordenar_index(df, lambda x: DIAS_ORDEM.index(x))
        return self.grafico_de_barras(df)

        print(df)
    def ordenar_index(self, df, key):
        df['sort_param'] = np.vectorize(key)(df.index)
        return df.sort_values('sort_param').drop('sort_param', 1)

    def grafico_de_barras(self, df):
        series = []
        for col in df.columns:
            series.append({
                'name': col,
                'data': df[col].values
            })
        return {
            'chartOptions': {
                'chart': {
                    'id': 'vuechart-example'
                },
                'xaxis': {'categories': df.index}
            },
            'series': series
        } 
class BoxPlotPorTrecho(BaseData):

    tipo_ponto = 'ponto_embarque__ponto__trecho__nome'
    
    columns = ['id', 'ponto_embarque__ponto__trecho__nome', 'partida_id']

    def calcular(self):
        df = self.get_df()
        pontos = df[self.tipo_ponto].unique()
        N = len(pontos)
        c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]

        data=[dict(
            name=pontos[i],
            y=df[df[self.tipo_ponto]==pontos[i]].groupby('partida_id').count()['id'].values,
            type='box',
            marker={
                'color': c[i]
            }) for i in range(int(N))]
        layout = {
            'xaxis': {
                'showgrid': False,
                'zeroline': False,
                'tickangle': 60,
                'showticklabels': False
            },
            'yaxis': {
                'zeroline': False,
                'gridcolor': 'white'
            },
            'paper_bgcolor': 'rgb(255,255,255)',
            'plot_bgcolor': 'rgb(255,255,255)',
            'showlegend':True
        }
        '''print({
            'data': data,
            'layout': layout
        })'''
        return {
            'data': data,
            'layout': layout
        }

    
        
class DadosPorHoraDoDia(BaseData):
    
    columns = ['id', 'horario']

    def calcular(self):
        df = self.get_df()
        df.index = pd.to_datetime(df['horario'])
        df = df.groupby(pd.Grouper(freq='10Min')).count()
        df['time'] = (pd.to_datetime(df.index) + pd.Timedelta(hours=-3)).time
        df = df.groupby('time').mean()
        df = df[['id',]]
        df.index = ('2010-01-01 '+df.index.to_series().astype(str)).apply(pd.Timestamp)
        df.columns = ['Passageiros']
        df = self.ordenar_index(df, lambda x: x)
        return self.grafico_de_area(df)

    def ordenar_index(self, df, key):
        df['sort_param'] = np.vectorize(key)(df.index)
        return df.sort_values('sort_param').drop('sort_param', 1)

    def grafico_de_area(self, df):
        series = []
        for col in df.columns:
            series.append({
                'name': col,
                'data': list(zip(df.index, df[col].values))
            })
        return {
            'chartOptions': {
                'chart': {
                    'id': 'area-datetime',
                    'type': 'area',
                    'height': 350,
                    'zoom': {
                        'autoScaleYaxis': True
                    }
                },
                'xaxis': {
                    'labels': {
                        'format': 'HH:mm',
                    },
                    
                    'type': 'datetime',
                },
                'dataLabels': {
                    'enabled': False
                },
                'markers': {
                    'size': 0,
                    'style': 'hollow',
                },
                'fill': {
                    'type': 'gradient',
                    'gradient': {
                        'shadeIntensity': 1,
                        'opacityFrom': 0.7,
                        'opacityTo': 0.9,
                        'stops': [0, 100]
                    }
                },
                'tooltip': {
                    'x': {
                        'show': True,
                        'format': 'HH:mm',
                      
                    }
                
                },
            },
            'series': series
        } 
    



