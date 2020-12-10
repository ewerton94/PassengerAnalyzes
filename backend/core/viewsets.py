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
