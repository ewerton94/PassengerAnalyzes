# Generated by Django 2.2 on 2021-01-06 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_viagemdepassageiro_linha'),
    ]

    operations = [
        migrations.AddField(
            model_name='linha',
            name='eixo',
            field=models.CharField(default='', max_length=500),
        ),
    ]
