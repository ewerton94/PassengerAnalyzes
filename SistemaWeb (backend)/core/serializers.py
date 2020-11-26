from rest_framework import serializers
from .models import *

'''
As classes desse arquivo realizam a serialização de cada classe do ./models.py (cada 'tabela') para a API local.

'''
class EmpresaSerializer(serializers.ModelSerializer):
    #logo = serializers.FileField(use_url=True)
    class Meta:
        model = Empresa
        fields = ["id", "nome"] 

class LinhaSerializer(serializers.ModelSerializer):
    #empresa = EmpresaSerializer(many=False, read_only=True)
    #inicio = ParadaSerializer(many=False, read_only=True)
    #fim = ParadaSerializer(many=False, read_only=True)
    class Meta:
        model = Linha
        fields = ["numero", "empresa"]
