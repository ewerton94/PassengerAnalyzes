from django.contrib import admin
from .models import *

admin.site.register(Empresa)
admin.site.register(Linha)
admin.site.register(Ponto)
admin.site.register(PontoPorEmpresa)
admin.site.register(TipoCartao)
# Register your models here.
