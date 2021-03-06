# Generated by Django 2.2 on 2020-12-22 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20201219_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='embarqueportrecho',
            name='ordem_trecho',
        ),
        migrations.RemoveField(
            model_name='embarqueportrecho',
            name='quantidade_no_veiculo_final_trecho',
        ),
        migrations.RemoveField(
            model_name='embarqueportrecho',
            name='sentido',
        ),
        migrations.RemoveField(
            model_name='embarqueportrecho',
            name='trecho',
        ),
        migrations.AddField(
            model_name='embarqueportrecho',
            name='ordem_ponto',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='embarqueportrecho',
            name='partida',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='por_trecho', to='core.Partida'),
        ),
        migrations.AddField(
            model_name='embarqueportrecho',
            name='ponto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='viagens', to='core.Ponto'),
        ),
        migrations.AddField(
            model_name='embarqueportrecho',
            name='quantidade_no_veiculo_pos_ponto',
            field=models.FloatField(default=0),
        ),
    ]
