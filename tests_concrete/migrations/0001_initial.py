# Generated by Django 2.2.5 on 2020-03-09 03:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('construction', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0001_initial'),
        ('reference_person', '0001_initial'),
        ('equipments', '0001_initial'),
        ('tools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrismBreak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prism_type', models.CharField(choices=[('DADO_GROUT', 'Dado de Grout'), ('DADO_CAL', 'Dado de Cal'), ('ADOQUIN_CONCRETO', 'Adoquin de Concreto')], default='DADO_GROUT', max_length=20)),
                ('sampling_date', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('name', models.CharField(default='Rotura Testigo', max_length=50)),
                ('code', models.CharField(editable=False, max_length=255, unique=True)),
                ('fc_esp', models.FloatField(default=280)),
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
            name='Prism',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poured_date', models.DateField()),
                ('break_date', models.DateField()),
                ('dilate', models.IntegerField(editable=False)),
                ('element_name', models.CharField(blank=True, max_length=100, null=True)),
                ('D_1', models.FloatField()),
                ('D_2', models.FloatField()),
                ('area', models.FloatField(editable=False)),
                ('load', models.FloatField()),
                ('fc', models.FloatField(editable=False)),
                ('fc_MPa', models.FloatField(editable=False)),
                ('fc_175', models.FloatField(editable=False)),
                ('fc_210', models.FloatField(editable=False)),
                ('fc_280', models.FloatField(editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('equipment', models.ManyToManyField(to='equipments.Equip')),
                ('prism_break', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests_concrete.PrismBreak')),
                ('tool', models.ManyToManyField(to='tools.Tool')),
            ],
        ),
        migrations.CreateModel(
            name='PiceBreak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pice_type', models.CharField(choices=[('CONCRETO', 'Testigo de Concreto'), ('CAL', 'Testigo de Cal')], default='CONCRETO', max_length=10)),
                ('sampling_date', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('name', models.CharField(default='Rotura Testigo', max_length=50)),
                ('code', models.CharField(editable=False, max_length=255, unique=True)),
                ('fc_esp', models.FloatField(default=280)),
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
            name='Pice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poured_date', models.DateField()),
                ('break_date', models.DateField()),
                ('dilate', models.IntegerField(editable=False)),
                ('element_name', models.CharField(blank=True, max_length=100, null=True)),
                ('D_1', models.FloatField()),
                ('D_2', models.FloatField()),
                ('area', models.FloatField(editable=False)),
                ('load', models.FloatField()),
                ('fc', models.FloatField(editable=False)),
                ('fc_MPa', models.FloatField(editable=False)),
                ('fc_175', models.FloatField(editable=False)),
                ('fc_210', models.FloatField(editable=False)),
                ('fc_280', models.FloatField(editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('equipment', models.ManyToManyField(to='equipments.Equip')),
                ('pice_break', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests_concrete.PiceBreak')),
                ('tool', models.ManyToManyField(to='tools.Tool')),
            ],
        ),
        migrations.CreateModel(
            name='DiamondPiceBreak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Compresión Testigo Diamantinos', max_length=50)),
                ('code', models.CharField(editable=False, max_length=255, unique=True)),
                ('fc_esp', models.FloatField(default=280)),
                ('sampling_date', models.DateField(blank=True, null=True)),
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
            name='DiamondPice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extraction_date', models.DateField()),
                ('break_date', models.DateField()),
                ('dilate', models.IntegerField(editable=False)),
                ('element_name', models.CharField(blank=True, max_length=100, null=True)),
                ('D', models.FloatField()),
                ('L', models.FloatField()),
                ('factor_ld', models.FloatField(editable=False)),
                ('area', models.FloatField(editable=False)),
                ('correction', models.FloatField(editable=False)),
                ('load', models.FloatField()),
                ('fc', models.FloatField(editable=False)),
                ('fc_MPa', models.FloatField(editable=False)),
                ('fc_175', models.FloatField(editable=False)),
                ('fc_210', models.FloatField(editable=False)),
                ('fc_280', models.FloatField(editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('diamond_pice_break', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests_concrete.DiamondPiceBreak')),
                ('equipment', models.ManyToManyField(to='equipments.Equip')),
                ('tool', models.ManyToManyField(to='tools.Tool')),
            ],
        ),
    ]
