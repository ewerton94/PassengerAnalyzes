# Generated by Django 2.2 on 2020-12-19 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20201218_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemtrechoslinha',
            name='atendimento',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='ordemtrechoslinha',
            name='sentido',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
