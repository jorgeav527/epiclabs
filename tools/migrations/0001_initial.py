# Generated by Django 2.2.5 on 2019-10-19 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('shop_day', models.DateField(blank=True, null=True)),
                ('last_maintenance_day', models.DateField(blank=True, null=True)),
                ('next_maintenance_day', models.DateField(blank=True, null=True)),
                ('maintenance_done', models.BooleanField(default=False)),
                ('use', models.IntegerField(default=0)),
            ],
        ),
    ]