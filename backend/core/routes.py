from rest_framework import routers, serializers, viewsets
from rest_framework.routers import DefaultRouter
from . import viewsets
'''
Definição dos endpoints.

'''

router = DefaultRouter()

router.register(r'empresas', viewsets.EmpresaViewSet)
#router.register(r'paradas', viewsets.ParadaViewSet)
router.register(r'linhas', viewsets.LinhaViewSet)
#router.register(r'viagens', viewsets.ViagemViewSet)
