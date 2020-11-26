# Generated by Django 2.2 on 2020-11-25 18:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=500)),
                ('placa', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Cartao',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('numero', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_oficial', models.CharField(max_length=500)),
                ('nome_cittamobi', models.CharField(max_length=500)),
                ('nome_report', models.CharField(max_length=500)),
                ('lote', models.CharField(max_length=500)),
                ('abreviacao', models.CharField(max_length=500)),
                ('ativa', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Linha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=500)),
                ('nome', models.CharField(max_length=500)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Partida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atendimento', models.CharField(blank=True, max_length=500, null=True)),
                ('horario_prevista_terminal', models.DateTimeField(blank=True, null=True)),
                ('horario_realizada_terminal', models.DateTimeField(blank=True, null=True)),
                ('somente_cartao', models.BooleanField(default=False)),
                ('sentido', models.CharField(blank=True, max_length=500, null=True)),
                ('real', models.BooleanField(default=True)),
                ('carro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidas', to='core.Carro')),
                ('linha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidas', to='core.Linha')),
            ],
        ),
        migrations.CreateModel(
            name='Ponto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('endereco', models.TextField()),
                ('endereco_cittamobi', models.TextField()),
                ('endereco_unico', models.BooleanField(default=False)),
                ('codigo', models.CharField(max_length=500)),
                ('bairro', models.TextField()),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PontoPorEmpresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_cittamobi', models.CharField(max_length=500)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Empresa')),
                ('ponto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pontos_por_empresa', to='core.Ponto')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TipoCartao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=500)),
                ('valor', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Trecho',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ViagemDePassageiro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario', models.DateTimeField()),
                ('integracao', models.BooleanField(default=False)),
                ('cartao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viagens_de_passageiros', to='core.Cartao')),
                ('partida', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='viagens_de_passageiros', to='core.Partida')),
                ('ponto_desembarque', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='desembarques', to='core.PontoPorEmpresa')),
                ('ponto_embarque', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='embarques', to='core.PontoPorEmpresa')),
            ],
        ),
        migrations.AddField(
            model_name='ponto',
            name='trecho',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pontos', to='core.Trecho'),
        ),
        migrations.CreateModel(
            name='OrdemTrechosLinha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordem', models.IntegerField()),
                ('linha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordens_trechos', to='core.Linha')),
                ('trecho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordens_linhas', to='core.Trecho')),
            ],
        ),
        migrations.CreateModel(
            name='LinhaPorDiaSemana',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.CharField(blank=True, max_length=500, null=True)),
                ('sentido', models.CharField(blank=True, max_length=500, null=True)),
                ('faixa_horaria', models.CharField(blank=True, max_length=500, null=True)),
                ('quantidade_total', models.FloatField()),
                ('quantidade_equivalente', models.FloatField()),
                ('linha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='por_dia_semana', to='core.Linha')),
            ],
        ),
        migrations.CreateModel(
            name='EmbarquePorTrecho',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentido', models.CharField(blank=True, max_length=500, null=True)),
                ('faixa_horaria', models.CharField(blank=True, max_length=500, null=True)),
                ('tempo_partida', models.TimeField()),
                ('quantidade_total_embarque', models.FloatField()),
                ('quantidade_total_desembarque', models.FloatField()),
                ('quantidade_no_veiculo_final_trecho', models.FloatField()),
                ('linha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='por_trecho', to='core.Linha')),
                ('trecho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viagens', to='core.Trecho')),
            ],
        ),
        migrations.CreateModel(
            name='EmbarqueDeLinhaPorTempo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentido', models.CharField(blank=True, max_length=500, null=True)),
                ('faixa_horaria', models.CharField(blank=True, max_length=500, null=True)),
                ('tempo_embarque', models.TimeField()),
                ('quantidade_total', models.FloatField()),
                ('quantidade_equivalente', models.FloatField()),
                ('linha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='por_tempo', to='core.Linha')),
            ],
        ),
        migrations.AddField(
            model_name='cartao',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartoes', to='core.TipoCartao'),
        ),
        migrations.AddField(
            model_name='carro',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Empresa'),
        ),
        migrations.AddField(
            model_name='carro',
            name='ultimo_carro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carro_futuro', to='core.Carro'),
        ),
    ]