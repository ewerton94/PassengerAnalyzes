from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from conf.permissions import CustomPermission
from .serializers import *
from .models import *
from .dataframe import *
import pandas as pd
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes, parser_classes

'''
As classes desse arquivo realizam um query (queryset = Model.objects.all()) dos Models e retornar essa requisição para o usuário
no formato serializado (serializer_class = ModelSerializer) definido em ./serializers.py.

'''

class EmpresaViewSet(viewsets.ModelViewSet):
    
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.AllowAny]

    http_method_names = ['get', 'post', 'options', 'head', 'put', 'update', 'delete']
    
    @action(detail=True,  methods=['get',])
    def linhas_por_empresa(self, request, pk=None):
        '''
        Realizar consulta das linhas de determinada Empresa.
        Obs.: PK = Id a empresa
        '''
            
        linhas = Linha.objects.all().filter(empresa=pk)
        linhas = LinhaSerializer(linhas, many=True)
        
        return Response(linhas.data)


class LinhaViewSet(viewsets.ModelViewSet):
    
    queryset = Linha.objects.all()
    serializer_class = LinhaSerializer
    permission_classes = [permissions.AllowAny]

    http_method_names = ['get', 'post', 'options', 'head', 'put', 'update', 'delete']

    @action(detail=False,  methods=['post',])
    def atualizar_info_linha(self, request, pk=None):
        '''
        Criar uma Linha e salvar no banco.
        '''    
        data = request.data
        print(data)
        
        return Response(status=status.HTTP_201_CREATED)
    
    @action(detail=False,  methods=['get',])
    def grafico(self, request, pk=None):
        ''''''
        linhas = request.GET.get('linhas')
        if linhas is None:
            return Response(status=status.HTTP_201_CREATED)
        linhas = linhas.split(',')
        tipo_grafico = request.GET.get('tipo_grafico')
        if tipo_grafico is None:
            return Response(status=status.HTTP_201_CREATED)
        viagens = ViagemDePassageiro.objects.filter(partida__linha__numero__in=linhas)
        viagens = self.qs_extra_filtro(viagens, request.GET)
        return Response(eval(tipo_grafico+'(viagens).calcular()'))
    
    def qs_extra_filtro(self, qs, params):
        if 'data_inicial' in params and 'data_final' in params:
            print(params.get('data_inicial'))
            print(params.get('data_final'))
            qs = qs.filter(
                partida__horario_prevista_terminal__date__gte=params.get('data_inicial'),
                partida__horario_prevista_terminal__date__lte=params.get('data_final')
            )
        if 'partida_inicial' in params and 'partida_final' in params:
            print(params.get('partida_inicial'))
            print(params.get('partida_final'))
            qs = qs.filter(
                partida__horario_prevista_terminal__time__gte=params.get('partida_inicial')+':00',
                partida__horario_prevista_terminal__time__lte=params.get('partida_final')+':00'
            )
        if 'embarque_inicial' in params and 'embarque_final' in params:
            print(params.get('embarque_inicial'))
            print(params.get('embarque_final'))
            qs = qs.filter(
                horario__time__gte=params.get('embarque_inicial'),
                horario__time__lte=params.get('embarque_final')
            )
        if 'sentido' in params:
            sentido = params.get('sentido')
            if sentido != 'AMBOS':
                qs = qs.filter(partida__sentido=sentido.lower())


        return qs
 
    @action(detail=False,  methods=['get',])
    def detalhar(self, request, pk=None):
        '''
        Criar uma Linha e salvar no banco.
        '''    
        print(request.GET)
        linhas = request.GET.get('linhas')
        if linhas is None:
            return Response(status=status.HTTP_201_CREATED)
        linhas = linhas.split(',')
        viagens = ViagemDePassageiro.objects.filter(partida__linha__numero__in=linhas)
        viagens = self.qs_extra_filtro(viagens, request.GET)
        viagens = DadosResumo(viagens).get_df()

        detail = {
            'passageiros': len(viagens['id'].unique()),
            'viagens': len(viagens['partida_id'].unique()),
            'numero': '...',
            'linha': 'Várias',
            'lote': '...',
            'empresa': 'Várias'
        }
        if len(linhas) == 1:
            linha = Linha.objects.get(numero=linhas[0])
            detail['numero'] = linha.numero
            detail['linha'] = linha.nome
            detail['lote'] = linha.empresa.lote
            detail['empresa'] = linha.empresa.nome_oficial
            
        print(detail)

        
        return Response(detail)

    
