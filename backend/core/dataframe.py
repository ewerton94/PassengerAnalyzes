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
    columns = ['id', 'partida_embarque_id']

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
    columns = ['id', 'cartao_id', 'partida_embarque_id', 'partida_embarque__sentido','horario', 'ponto_embarque__ponto__codigo', 'partida_embarque__linha_id', 'partida_embarque__atendimento', 'ponto_embarque__ponto_id']
    names = ['id', 'cartao', 'partida_embarque', 'sentido', 'horario', 'ponto', 'linha', 'atendimento', 'ponto_id']

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
            df['next_partida_embarque'] = df['partida_embarque'].shift(-1)
            df = df[df['ponto'].shift(-1) != df['ponto']]
            df = df[df['partida_embarque'].shift(-1) != df['partida_embarque']]
            df.loc[df['cartao'].shift(-1) != df['cartao'], ['next_ponto', 'next_ponto_id', 'next_partida_embarque', 'next_sentido']] = np.nan
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
            partida_embarques = Partida.objects.all().values_list('id', 'horario_prevista_terminal', 'carro_id')
            partida_embarques = pd.DataFrame(list(partida_embarques), columns=['id', 'partida_embarque', 'carro'])
            partida_embarques = partida_embarques.sort_values(by=['carro', 'partida_embarque'])
            partida_embarques['next_partida_embarque'] = partida_embarques['id'].shift(-1)
            print('partida_embarque')
            print(partida_embarques)
            partida_embarques = {id_: next_ for id_, next_ in zip(partida_embarques.id.values, partida_embarques.next_partida_embarque.values)}
            #print('partida_embarques')
            #print(partida_embarques)
            nex_partida_embarque = {}
            print(df)
            
            df = df[['id', 'ordem', 'next_ponto_id', 'next_ordem', 'partida_embarque', 'sentido']]
            df.loc[:, 'coordenadas'] = df['next_ponto_id'].map(dic_pontos)
            df['closest'] = [closest_point(x, list(df_pontos[df_pontos['ordem']>omin]['coordenadas'])) for x, omin in zip(df['coordenadas'], df['ordem'])]
            df = df[~pd.isnull(df.closest)]
            #print(dic_coordenadas)
            df['desembarque_id'] = df['closest'].apply(lambda x: dic_coordenadas[(x[0], x[1], 2)])
            df['desembarque_ordem'] = df['desembarque_id'].map(dic_pontos_ordem)
            print(df[['partida_embarque', 'ordem', 'desembarque_ordem']])
            filtro = (df['desembarque_ordem'] > 1000) & (df['sentido'] == 'ida')
            print(df.loc[filtro, 'partida_embarque'])
            df.loc[filtro, 'partida_embarque'] = df.loc[filtro, 'partida_embarque'].map(partida_embarques)
            print(df.loc[filtro, 'partida_embarque'])



            #df2['closest'] = [closest_point(x, list(df1['point'])) for x in df2['point']]
            #df['cartao'] = df['cartao'].astype(str).apply(lambda x: x[:6])
            #df = df[['cartao', 'partida_embarque', 'horario', 'ponto', 'next_ponto']]
            #df['next_cartao'] = df['cartao'].shift(-1)
            print(df.columns)
            print(df[['partida_embarque', 'ordem', 'desembarque_ordem']])
            df = df[df.desembarque_ordem > df.ordem]
            print(df.loc[pd.isnull(df.partida_embarque), ['partida_embarque', 'ordem', 'desembarque_ordem']])
            df = df.dropna(subset=['partida_embarque'])
            vs = self.queryset.filter(id__in=df.id.values)
            for v in vs:
                v.ponto_desembarque_id = int(df.loc[df.id == v.id, 'desembarque_id'])
                #print(int(df.loc[df.id == v.id, 'partida_embarque']))
                #print(df.loc[df.id == v.id, :])
                '''
                if v.partida_embarque_id !=  int(df.loc[df.id == v.id, 'partida_embarque']):
                    p = Partida_embarque.objects.get(id=int(df.loc[df.id == v.id, 'partida_embarque']))
                    print(v.horario, v.partida_embarque.horario_realizada_terminal, v.partida_embarque.sentido, p.horario_realizada_terminal, p.sentido)
                    eeeee
                '''

                v.partida_desembarque_id = int(df.loc[df.id == v.id, 'partida_embarque'])
            #errrr
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
    o = ordem_ponto.get((x[0], x[1]), None)
    print(x)
    if o is None:
        o = ordem_ponto.get((x[0], inverso[x[1]]), -1)
    if x[1] == 'volta':
        o = o + 1000 
    return o

def get_a_trocar_sentido(ordem_ponto, x):
    return ordem_ponto.get((x[0], x[1]), np.nan)

    
class BoxPlotPorTrecho(BaseData):

    tipo_ponto = 'ponto_embarque__ponto__trecho__nome'
    
    columns = ['id', 'ponto_embarque__ponto__trecho__nome', 'partida_embarque_id', 'ponto_embarque__ponto_id', 'partida_embarque__sentido']

    def calcular(self):
        df = self.get_df()
        ordem_ponto = {(p, s): o for p, o, s in OrdemPontosLinha.objects.select_related().all().values_list('ponto__trecho__nome', 'ordem', 'sentido').distinct()}
        un = df[[self.tipo_ponto, 'partida_embarque__sentido']].drop_duplicates()
        #print(list(zip(df[self.tipo_ponto].values, df.partida_embarque__sentido.values)))
        print('Antes', self.tipo_ponto)
        pontos = [ee for ee in sorted(list(set(list(zip(un[self.tipo_ponto].values, un.partida_embarque__sentido.values)))), key=lambda x: get_order_trecho(ordem_ponto, x)) if not ee[0] is None]
        print('Depois', self.tipo_ponto)
        N = len(pontos)
        print(N, self.tipo_ponto)
        print(N, pontos, self.tipo_ponto)
        c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]

        data=[dict(
            name=str(i+1) + ' - ' +pontos[i][0] + ' (%s)'%(pontos[i][1][0].upper()),
            y=df[(df[self.tipo_ponto]==pontos[i][0]) & (df['partida_embarque__sentido']==pontos[i][1])].groupby('partida_embarque_id').count()['id'].values,
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
    
    columns = ['id', 'ponto_desembarque__ponto__trecho__nome', 'partida_desembarque_id', 'ponto_desembarque__ponto_id', 'partida_desembarque__sentido']   
    def calcular(self):
        self.queryset = self.queryset.filter(partida_desembarque__isnull=False)
        df = self.get_df()
        ordem_ponto = {(p, s): o for p, o, s in OrdemPontosLinha.objects.select_related().all().values_list('ponto__trecho__nome', 'ordem', 'sentido').distinct()}
        #print(list(zip(df[self.tipo_ponto].values, df.partida_desembarque__sentido.values)))
        print('Antes', self.tipo_ponto)
        df['trocar'] = [get_a_trocar_sentido(ordem_ponto, ee) for ee in list(zip(df[self.tipo_ponto].values, df.partida_desembarque__sentido.values))]
        df.loc[pd.isnull(df['trocar']), 'partida_desembarque__sentido'] = df.loc[pd.isnull(df['trocar']), 'partida_desembarque__sentido'].map({'ida': 'volta', 'volta': 'ida'})
        un = df[[self.tipo_ponto, 'partida_desembarque__sentido']].drop_duplicates()
        pontos = [ee for ee in sorted(list(set(list(zip(un[self.tipo_ponto].values, un.partida_desembarque__sentido.values)))), key=lambda x: get_order_trecho(ordem_ponto, x)) if not ee[0] is None]
        print('Depois', self.tipo_ponto)
        N = len(pontos)
        print(N, self.tipo_ponto)
        print(N, pontos, self.tipo_ponto)
        c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]

        data=[dict(
            name=str(i+1) + ' - ' +pontos[i][0] + ' (%s)'%(pontos[i][1][0].upper()),
            y=df[(df[self.tipo_ponto]==pontos[i][0]) & (df['partida_desembarque__sentido']==pontos[i][1])].groupby('partida_desembarque_id').count()['id'].values,
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
class MapaCalorEmbarque(BoxPlotPorTrecho):

    tipo_ponto = 'ponto_desembarque__ponto__lat'
    
    columns = ['ponto_embarque__ponto__lat', 'ponto_embarque__ponto__lon']   
    def calcular(self):
        self.queryset = self.queryset.filter(partida_desembarque__isnull=False)
        df = self.get_df()
        lat, lng = df['ponto_embarque__ponto__lat'].mean(), df['ponto_embarque__ponto__lon'].mean()
        pontos = [{'lat': lat, 'lng': lon} for lat, lon in zip(df.ponto_embarque__ponto__lat.values, df.ponto_embarque__ponto__lon.values)]
        print('lat, lng' )
        print(lat, lng )
        return {
            'data': pontos,
            'lat': lat,
            'lng': lng,
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
    



