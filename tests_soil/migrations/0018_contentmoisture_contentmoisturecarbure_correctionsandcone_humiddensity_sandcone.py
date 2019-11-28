# Generated by Django 2.2.5 on 2019-11-26 03:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reference_person', '0007_auto_20191023_1837'),
        ('construction', '0003_remove_construction_reference'),
        ('equipments', '0001_initial'),
        ('course', '0002_auto_20191018_2305'),
        ('tests_soil', '0017_granulometricglobal'),
    ]

    operations = [
        migrations.CreateModel(
            name='SandCone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Sand Cone', max_length=50)),
                ('material', models.CharField(max_length=50)),
                ('sampling_name', models.CharField(max_length=50)),
                ('progressive_sector', models.CharField(max_length=50)),
                ('section_level', models.CharField(max_length=50)),
                ('element_side', models.CharField(max_length=50)),
                ('layer', models.CharField(max_length=50)),
                ('weight_dry_max', models.FloatField()),
                ('opt_moisture', models.FloatField()),
                ('moisture', models.BooleanField(default=False)),
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
            name='HumidDensity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bowl_weight_sand', models.IntegerField()),
                ('bowl_weight_remaining_sand', models.IntegerField()),
                ('weight_sand', models.IntegerField(editable=False)),
                ('weight_sand_cone_plate', models.IntegerField()),
                ('weight_sand_excavation', models.IntegerField(editable=False)),
                ('sand_density', models.FloatField()),
                ('volume_material_extracted', models.IntegerField(editable=False)),
                ('sample_weight_container', models.IntegerField()),
                ('container_weight', models.IntegerField(default=0)),
                ('wet_sample_weight', models.IntegerField(editable=False)),
                ('density_wet_sample', models.FloatField(editable=False)),
                ('equipment', models.ManyToManyField(to='equipments.Equip')),
                ('sand_cone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests_soil.SandCone')),
                ('tool', models.ManyToManyField(to='tools.Tool')),
            ],
        ),
        migrations.CreateModel(
            name='CorrectionSandCone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wet_fraction_weight', models.IntegerField()),
                ('p_e_ap_frac_extrad', models.FloatField()),
                ('per_abs_tails_extrad', models.FloatField()),
                ('weight_fraction_extrad', models.FloatField(editable=False)),
                ('equipment', models.ManyToManyField(to='equipments.Equip')),
                ('sand_cone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests_soil.SandCone')),
                ('tool', models.ManyToManyField(to='tools.Tool')),
            ],
        ),
        migrations.CreateModel(
            name='ContentMoistureCarbure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wet_weight_percentage', models.FloatField()),
                ('dry_weight_percentage', models.IntegerField()),
                ('equipment', models.ManyToManyField(to='equipments.Equip')),
                ('sand_cone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests_soil.SandCone')),
                ('tool', models.ManyToManyField(to='tools.Tool')),
            ],
        ),
        migrations.CreateModel(
            name='ContentMoisture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_fraction_pass', models.CharField(default='Pas. 3/4"', max_length=15)),
                ('bowl_weight', models.FloatField()),
                ('wet_sample_weight_bowl', models.FloatField()),
                ('dry_sample_weight_bowl', models.FloatField()),
                ('weight_water', models.FloatField(editable=False)),
                ('dry_sample_weight', models.FloatField(editable=False)),
                ('sample_moisture', models.FloatField(editable=False)),
                ('equipment', models.ManyToManyField(to='equipments.Equip')),
                ('sand_cone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests_soil.SandCone')),
                ('tool', models.ManyToManyField(to='tools.Tool')),
            ],
        ),
    ]
