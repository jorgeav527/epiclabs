# Generated by Django 2.2.5 on 2019-11-14 04:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reference_person', '0007_auto_20191023_1837'),
        ('course', '0002_auto_20191018_2305'),
        ('tools', '0001_initial'),
        ('construction', '0003_remove_construction_reference'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equipments', '0001_initial'),
        ('tests_soil', '0007_finematerial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equivalent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Valor Equivalente Arena Finos', max_length=50)),
                ('pit', models.CharField(blank=True, max_length=50, null=True)),
                ('layer', models.CharField(choices=[('UNO', 'Estrato 1'), ('DOS', 'Estrato 2'), ('TRES', 'Estrato 3'), ('CUATRO', 'Estrato 4')], max_length=6)),
                ('code', models.CharField(editable=False, max_length=255, unique=True)),
                ('sampling_date', models.DateField()),
                ('done_date', models.DateField(default=datetime.datetime.now)),
                ('dilate', models.IntegerField(editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('construction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='construction.Construction')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.Course')),
                ('equipment', models.ManyToManyField(to='equipments.Equip')),
                ('reference_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reference_person.ReferencePerson')),
                ('tool', models.ManyToManyField(to='tools.Tool')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Equiv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_size', models.FloatField(default=4.75)),
                ('start_sat_time', models.TimeField()),
                ('out_sat_time', models.TimeField()),
                ('start_dec_time', models.TimeField()),
                ('out_dec_time', models.TimeField()),
                ('max_high_fine', models.FloatField()),
                ('max_high_sand', models.FloatField()),
                ('equiv_sand', models.FloatField(editable=False)),
                ('equipment', models.ManyToManyField(to='equipments.Equip')),
                ('equivalent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests_soil.Equivalent')),
                ('tool', models.ManyToManyField(to='tools.Tool')),
            ],
        ),
    ]