from core.models import *

for linha, num in Linha.objects.all().values_list('id', 'numero'):
    total = ViagemDePassageiro.objects.filter(linha_id=linha).count()
    total_dinheiro = ViagemDePassageiro.objects.filter(linha_id=linha, cartao__tipo__tipo='BOTOEIRAS').count()
    total_embarque = ViagemDePassageiro.objects.filter(linha_id=linha, partida_embarque__isnull=False).count()
    total_desembarque = ViagemDePassageiro.objects.filter(linha_id=linha, partida_desembarque__isnull=False).count()
    print('\n\n------------\nLinha:', num)
    if total == 0:
        print('Sem passageiros')
        Linha.objects.filter(id=linha).delete()
    else:
        print('Total | Dinheiro | Embarque | Desembarque')
        print(total, total_dinheiro, total_embarque, total_desembarque)
        print(total, 100-100*total_dinheiro/total, 100*total_embarque/total, 100*total_desembarque/total)

