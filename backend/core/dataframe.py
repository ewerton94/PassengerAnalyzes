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

def get_order(dic_ordem, a, b, c, d):
    o = dic_ordem.get((a, b, c, d), -1)
    if d == 'volta' and o >=0:
        o += 1000
    return o
from scipy.spatial.distance import cdist

def closest_point(point, points):
    """ Find closest point from a list of points. """
    #print(len(point), len(points))
    if len(points) > 0:
        return points[cdist([point], points).argmin()]
    return np.nan
from bulk_update.helper import bulk_update
class CalcularDesembarque(BaseData):
    columns = ['id', 'cartao_id', 'partida_id', 'partida__sentido','horario', 'ponto_embarque__ponto__codigo', 'partida__linha_id', 'partida__atendimento', 'ponto_embarque__ponto_id']
    names = ['id', 'cartao', 'partida', 'sentido', 'horario', 'ponto', 'linha', 'atendimento', 'ponto_id']

    def calcular(self):
        self.queryset = self.queryset.filter(calculou_ponto_desembarque=False)
        if self.queryset.exists():
            df = self.get_df()
            df.columns = self.names
            df = df.sort_values(by=['cartao', 'horario'])
            df['data'] = df['horario'].dt.date
            df = df[df.groupby(['cartao', 'data'])['horario'].transform('count') > 1]
            df['next_ponto'] = df['ponto'].shift(-1)
            df['next_ponto_id'] = df['ponto_id'].shift(-1)
            df['next_sentido'] = df['sentido'].shift(-1)
            df['next_partida'] = df['partida'].shift(-1)
            df = df[df['ponto'].shift(-1) != df['ponto']]
            df = df[df['partida'].shift(-1) != df['partida']]
            df.loc[df['cartao'].shift(-1) != df['cartao'], ['next_ponto', 'next_ponto_id', 'next_partida', 'next_sentido']] = np.nan
            df = df[df.groupby(['cartao', 'data'])['horario'].transform('count') > 1]
            for cartao, df_ in  df[['cartao', 'ponto', 'next_ponto', 'next_ponto_id','sentido', 'next_sentido']].groupby('cartao'):
                df.loc[df_.index[-1], ['next_ponto', 'next_ponto_id', 'next_sentido']] = list(df.loc[df_.index[0], ['ponto', 'ponto_id', 'sentido']].values)
            dic_ordem = {(o.ponto_id, o.linha_id, o.atendimento, o.sentido): o.ordem for o in OrdemPontosLinha.objects.all()}
            #print(dic_ordem.keys())
            df['ordem'] = np.vectorize(get_order)(dic_ordem, df['ponto_id'].astype(int).values, df['linha'].values, df['atendimento'].values, df['sentido'].values)
            df['next_ordem'] = np.vectorize(get_order)(dic_ordem, df['next_ponto_id'].astype(int).values, df['linha'].values, df['atendimento'].values, df['sentido'].values)
            dic_pontos_ordem = {p: o for p, o in zip(df['ponto_id'], df['ordem'])}
            dic_pontos = {p.id: (p.lat, p.lon) for p in Ponto.objects.all()}
            dic_coordenadas = {(lat, lon, c): id  for id, lat, lon, c in PontoPorEmpresa.objects.all().values_list('id', 'ponto__lat', 'ponto__lon', 'empresa_id').distinct()}
            #dic_coordenadas_ordem = {(p.lat, p.lon): p.id  for p in Ponto.objects.all()}
            df_pontos = df[['ponto_id', 'ordem', 'next_ponto_id', 'next_ordem']]
            df_pontos.loc[:, 'coordenadas']=df_pontos['ponto_id'].map(dic_pontos)
            
            df = df[['id', 'ordem', 'next_ponto_id', 'next_ordem']]
            df.loc[:, 'coordenadas'] = df['next_ponto_id'].map(dic_pontos)
            df['closest'] = [closest_point(x, list(df_pontos[df_pontos['ordem']>omin]['coordenadas'])) for x, omin in zip(df['coordenadas'], df['ordem'])]
            df = df[~pd.isnull(df.closest)]
            print(dic_coordenadas)
            df['desembarque_id'] = df['closest'].apply(lambda x: dic_coordenadas[(x[0], x[1], 2)])
            df['desembarque_ordem'] = df['desembarque_id'].map(dic_pontos_ordem)



            #df2['closest'] = [closest_point(x, list(df1['point'])) for x in df2['point']]
            #df['cartao'] = df['cartao'].astype(str).apply(lambda x: x[:6])
            #df = df[['cartao', 'partida', 'horario', 'ponto', 'next_ponto']]
            #df['next_cartao'] = df['cartao'].shift(-1)
            print(df.columns)
            print(df)
            df = df[df.desembarque_ordem > df.ordem]
            print(df)
            vs = self.queryset.filter(id__in=df.id.values)
            for v in vs:
                v.ponto_desembarque_id = int(df.loc[df.id == v.id, 'desembarque_id'])
            bulk_update(vs)
            self.queryset.update(calculou_ponto_desembarque=True)
            return True
        else: 
            return False
        

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


def get_order_trecho(ordem_ponto, x):
    inverso = {'ida': 'volta', 'volta': 'ida'}
    o = ordem_ponto.get((x[0], x[1]), ordem_ponto.get((x[0], inverso[x[1]]), -1))
    if x[1] == 'volta':
        o = o + 1000 
    return o
    
class BoxPlotPorTrecho(BaseData):

    tipo_ponto = 'ponto_embarque__ponto__trecho__nome'
    
    columns = ['id', 'ponto_embarque__ponto__trecho__nome', 'partida_id', 'ponto_embarque__ponto_id', 'partida__sentido']

    def calcular(self):
        df = self.get_df()
        ordem_ponto = {(p, s): o for p, o, s in OrdemPontosLinha.objects.select_related().all().values_list('ponto__trecho__nome', 'ordem', 'sentido').distinct()}
        un = df[[self.tipo_ponto, 'partida__sentido']].drop_duplicates()
        #print(list(zip(df[self.tipo_ponto].values, df.partida__sentido.values)))
        print('Antes', self.tipo_ponto)
        pontos = [ee for ee in sorted(list(set(list(zip(un[self.tipo_ponto].values, un.partida__sentido.values)))), key=lambda x: get_order_trecho(ordem_ponto, x)) if not ee[0] is None]
        print('Depois', self.tipo_ponto)
        N = len(pontos)
        print(N, self.tipo_ponto)
        print(N, pontos, self.tipo_ponto)
        c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]

        data=[dict(
            name=str(i+1) + ' - ' +pontos[i][0] + ' (%s)'%(pontos[i][1][0].upper()),
            y=df[(df[self.tipo_ponto]==pontos[i][0]) & (df['partida__sentido']==pontos[i][1])].groupby('partida_id').count()['id'].values,
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

    
class BoxPlotPorTrechoDesembarque(BoxPlotPorTrecho):

    tipo_ponto = 'ponto_desembarque__ponto__trecho__nome'
    
    columns = ['id', 'ponto_desembarque__ponto__trecho__nome', 'partida_id', 'ponto_desembarque__ponto_id', 'partida__sentido']   
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
    



