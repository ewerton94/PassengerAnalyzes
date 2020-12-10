import pandas as pd
import sys

nomes = [
    'ordem',
    'prefixo',
    'lugares',
    'data',
    'placa',
    'renavam',
    'chassi_numero',
    'chassi_data',
    'chassi_idade',
    'chassi_modelo',
    'chassi_fabricante',
    'carroceria_numero',
    'carroceria_layout',
    'carroceria_data',
    'carroceria_idade',
    'carroceria_modelo',
    'carroceria_fabricante',
    'motor_numero',
    'motor_data',
    'motor_idade',
    'motor_modelo',
    'motor_fabricante',
    'situacao',
    'elevador'
]

d = {'vele': 2}



from core.models import Empresa, Carro

empresa_por_abreviacao = {e.abreviacao: e for e in Empresa.objects.all()}

def create_car(line):
    global empresa_por_abreviacao
    empresa = empresa_por_abreviacao[line['empresa']]
    ultimo_carro = None
    
    c = Carro(
        empresa=empresa,
        ultimo_carro=ultimo_carro,
        numero = line['prefixo'],
        placa = line['placa'],
        
    )
    return c


    

'''   


    class Car(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    last_car = models.ForeignKey('self', related_name='future_car', on_delete=models.CASCADE)
    source_car = models.ForeignKey(SourceCar, on_delete=models.CASCADE)

    bodyworker = models.ForeignKey(Bodyworker, on_delete=models.CASCADE)
    chassis = models.ForeignKey(Chassis, on_delete=models.CASCADE)
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE)

    start_date = models.DateTimeField(auto_now_add=True)
    final_date = models.DateTimeField(auto_now_add=True)
    lift = models.BooleanField(default=False)

    prefix = models.CharField(max_length=500)
    plate = models.CharField(max_length=500)
    renavam = models.CharField(max_length=500)


'''





for empresa in ['cima', 'real', 'sfra', 'vele']:

    df = pd.read_excel('frota '+ empresa +'.xls', encoding='windows-1252', skiprows=d.get(empresa, 19), names=nomes).dropna(subset=['ordem',])
    df['empresa'] = empresa.upper()
    df['data'] = pd.to_datetime(df['data'])
    df = df[~pd.to_numeric(df['ordem'], errors='coerce').isnull()]
    cars = []
    for i, row in df.iterrows():
        #print(row)
        cars.append(create_car(row))
    Carro.objects.bulk_create(cars)
    
    print(df)
