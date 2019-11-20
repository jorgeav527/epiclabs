# Generated by Django 2.2.5 on 2019-11-16 00:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20191018_2305'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('construction', '0003_remove_construction_reference'),
        ('reference_person', '0007_auto_20191023_1837'),
        ('tools', '0001_initial'),
        ('equipments', '0001_initial'),
        ('tests_soil', '0009_auto_20191114_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProctorM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Proctor Modificado', max_length=50)),
                ('material', models.CharField(max_length=50)),
                ('quarry', models.CharField(max_length=50)),
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
            name='DensityWetDry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layers', models.IntegerField(default=5)),
                ('hits', models.IntegerField()),
                ('material_weight_P', models.IntegerField()),
                ('bowl_weight_P', models.IntegerField(default=6380)),
                ('compacted_weight_P', models.IntegerField(editable=False)),
                ('bowl_volume_P', models.FloatField(default=2130.0)),
                ('wet_density', models.FloatField(editable=False)),
                ('bowl', models.IntegerField()),
                ('bowl_weight', models.FloatField()),
                ('wet_weight', models.FloatField()),
                ('dry_weight', models.FloatField()),
                ('water_weight', models.FloatField(editable=False)),
                ('material_weight', models.FloatField(editable=False)),
                ('moisture', models.FloatField(editable=False)),
                ('dry_density', models.FloatField(editable=False)),
                ('equipment', models.ManyToManyField(to='equipments.Equip')),
                ('proctor_m', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests_soil.ProctorM')),
                ('tool', models.ManyToManyField(to='tools.Tool')),
            ],
        ),
    ]