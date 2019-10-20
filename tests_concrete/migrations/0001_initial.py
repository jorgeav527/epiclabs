# Generated by Django 2.2.5 on 2019-10-19 00:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('construction', '0001_initial'),
        ('reference_person', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tools', '0001_initial'),
        ('equipments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PiceBreak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Rotura de Testigo de Concreto', max_length=50)),
                ('code', models.CharField(editable=False, max_length=255, unique=True)),
                ('fc_esp', models.FloatField(default=280.0)),
                ('fecha_vaciado', models.DateField()),
                ('fecha_rotura', models.DateField(default=datetime.datetime.now)),
                ('edad', models.IntegerField(editable=False)),
                ('diameter_esp', models.FloatField(blank=True, choices=[(2, '2 Inch'), (4, '4 Inch'), (6, '6 Inch')], null=True)),
                ('diameter_1', models.FloatField(blank=True, null=True)),
                ('diameter_2', models.FloatField(blank=True, null=True)),
                ('area', models.FloatField(editable=False)),
                ('h', models.FloatField(default=15.0)),
                ('F', models.FloatField()),
                ('fc', models.FloatField(editable=False)),
                ('fc_MPa', models.FloatField(editable=False)),
                ('fc_175', models.FloatField(editable=False)),
                ('fc_210', models.FloatField(editable=False)),
                ('fc_280', models.FloatField(editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('construction', models.ManyToManyField(blank=True, to='construction.Construction')),
                ('equipment', models.ManyToManyField(to='equipments.Equip')),
                ('ref_person', models.ManyToManyField(blank=True, to='reference_person.ReferencePerson')),
                ('tool', models.ManyToManyField(to='tools.Tool')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
