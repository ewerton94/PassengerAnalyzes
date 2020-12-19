from django.db import models
import uuid

class TipoCartao(models.Model):
    tipo = models.CharField(max_length=500)
    valor = models.CharField(max_length=500)

class Cartao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero = models.CharField(max_length=500)
    tipo = models.ForeignKey(TipoCartao, on_delete=models.CASCADE, related_name='cartoes')

class Trecho(models.Model):
    nome = models.CharField(max_length=500)

class Ponto(models.Model):
    class Meta:
        ordering = ['id',]
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    trecho = models.ForeignKey(Trecho, on_delete=models.CASCADE, related_name='pontos', null=True, blank=True)
    endereco = models.TextField(default='')
    endereco_cittamobi = models.TextField(default='')
    endereco_unico = models.BooleanField(default=False)
    codigo = models.CharField(max_length=500)
    bairro = models.TextField(default='')

    def __str__(self):
        return "%i (%.4f, %.4f)"%(self.codigo, self.lat, self.lon)


class Empresa(models.Model):
    nome_oficial = models.CharField(max_length=500)
    nome_cittamobi = models.CharField(max_length=500)
    nome_report = models.CharField(max_length=500)
    lote = models.CharField(max_length=500)
    abreviacao = models.CharField(max_length=500)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_oficial

class PontoPorEmpresa(models.Model):
    class Meta:
        ordering = ['id',]
    ponto = models.ForeignKey(Ponto, on_delete=models.CASCADE, related_name='pontos_por_empresa', null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    codigo_cittamobi = models.CharField(max_length=500)
    
    def __str__(self):
        return str(self.ponto)
class Linha(models.Model):
    numero = models.CharField(max_length=500)
    nome = models.CharField(max_length=500)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class OrdemPontosLinha(models.Model):
    linha = models.ForeignKey(Linha, on_delete=models.CASCADE, related_name='ordens_trechos')
    ponto = models.ForeignKey(Ponto, on_delete=models.CASCADE, related_name='ordens_linhas')
    ordem = models.IntegerField()
    atendimento = models.CharField(max_length=500, null=True, blank=True)
    sentido = models.CharField(max_length=500, null=True, blank=True)

class Carro(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    ultimo_carro = models.ForeignKey('self', related_name='carro_futuro', on_delete=models.CASCADE, null=True)
    numero = models.CharField(max_length=500)
    placa = models.CharField(max_length=500)

class Partida(models.Model):
    linha = models.ForeignKey(Linha, on_delete=models.CASCADE, related_name='partidas')
    atendimento = models.CharField(max_length=500, null=True, blank=True)
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='partidas')
    horario_prevista_terminal = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    horario_realizada_terminal = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    somente_cartao = models.BooleanField(default=False)
    sentido = models.CharField(max_length=500, null=True, blank=True)
    real = models.BooleanField(default=True)

class ViagemDePassageiro(models.Model):
    cartao = models.ForeignKey(Cartao, on_delete=models.CASCADE, related_name='viagens_de_passageiros')
    ponto_embarque = models.ForeignKey(PontoPorEmpresa, on_delete=models.CASCADE, related_name='embarques', null=True, blank=True)
    ponto_desembarque = models.ForeignKey(PontoPorEmpresa, on_delete=models.CASCADE, related_name='desembarques', null=True, blank=True)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='viagens_de_passageiros', null=True, blank=True)
    horario = models.DateTimeField(auto_now_add=False)
    integracao = models.BooleanField(default=False)
    calculou_ponto_desembarque = models.BooleanField(default=False)

class LinhaPorDiaSemana(models.Model):
    linha = models.ForeignKey(Linha, on_delete=models.CASCADE, related_name='por_dia_semana')
    dia_semana = models.CharField(max_length=500, null=True, blank=True)
    sentido = models.CharField(max_length=500, null=True, blank=True)
    faixa_horaria = models.CharField(max_length=500, null=True, blank=True)
    quantidade_total = models.FloatField()
    quantidade_equivalente = models.FloatField()

class EmbarqueDeLinhaPorTempo(models.Model):
    linha = models.ForeignKey(Linha, on_delete=models.CASCADE, related_name='por_tempo')
    sentido = models.CharField(max_length=500, null=True, blank=True)
    faixa_horaria = models.CharField(max_length=500, null=True, blank=True)
    tempo_embarque = models.TimeField()
    quantidade_total = models.FloatField()
    quantidade_equivalente = models.FloatField()

class EmbarquePorTrecho(models.Model):
    linha = models.ForeignKey(Linha, on_delete=models.CASCADE, related_name='por_trecho')
    trecho = models.ForeignKey(Trecho, on_delete=models.CASCADE, related_name='viagens')
    sentido = models.CharField(max_length=500, null=True, blank=True)
    faixa_horaria = models.CharField(max_length=500, null=True, blank=True)
    tempo_partida = models.TimeField()
    quantidade_total_embarque = models.FloatField()
    quantidade_total_desembarque = models.FloatField()
    quantidade_no_veiculo_final_trecho = models.FloatField()
    ordem_trecho = models.IntegerField()

