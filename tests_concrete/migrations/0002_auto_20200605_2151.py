# Generated by Django 2.2.5 on 2020-06-06 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_concrete', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prismbreak',
            name='prism_type',
            field=models.CharField(choices=[('DADO_CONCRETO', 'Dado de Concreto'), ('DADO_CAL', 'Dado de Cal'), ('ROCA', 'Roca'), ('ADOQUIN_CONCRETO', 'Adoquin de Concreto')], default='DADO_CONCRETO', max_length=20),
        ),
    ]
