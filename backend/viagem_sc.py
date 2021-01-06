from core.models import *

Partida.objects.filter(atendimento__icontains='CARTÃO').update(somente_cartao=True)

ferwfewr