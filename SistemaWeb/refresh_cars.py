import pandas as pd
from core.models import Carro
for car in Carro.objects.all():
    car.numero = str(int(float(car.numero)))
    car.save()
existing = [c.numero for c in Carro.objects.all()]
files = [
    #'VEICULOS ATUAL VELEIRO.xlsx', 
    'VEICULOS ATUAL SFRA.xlsx',
    #'VEICULOS ATUAL REAL.xlsx',
    #'VEICULOS ATUAL CIMA.xlsx'
]
for file in files:
    cars = pd.read_excel(file)
    for i, car in cars.iterrows():
        carro = Carro.objects.filter(placa=car.Placa, ultimo_carro=None)
        if carro:
            carro=carro[0]
            pk = carro.pk
            carro.pk=None
            carro.numero = car.Prefixo
            carro.ultimo_carro_id=pk
            carro.save()
        else:
            Carro.objects.create(
                empresa_id=2,
                numero=car.Prefixo,
                placa=car.Placa
            )
