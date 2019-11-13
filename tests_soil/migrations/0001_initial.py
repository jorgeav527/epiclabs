# Generated by Django 2.2.5 on 2019-11-06 02:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tools', '0001_initial'),
        ('equipments', '0001_initial'),
        ('construction', '0003_remove_construction_reference'),
        ('reference_person', '0007_auto_20191023_1837'),
        ('course', '0002_auto_20191018_2305'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Limit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Limite Liquido Pastico', max_length=50)),
                ('pit', models.CharField(blank=True, max_length=50, null=True)),
                ('code', models.CharField(editable=False, max_length=255, unique=True)),
                ('extraction_data', models.DateField()),
                ('done_data', models.DateField(default=datetime.datetime.now)),
                ('duration', models.IntegerField(editable=False)),
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
    ]
