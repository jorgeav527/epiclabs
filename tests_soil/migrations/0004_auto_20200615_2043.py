# Generated by Django 2.2.5 on 2020-06-16 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_soil', '0003_auto_20200613_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='densitywetdry',
            name='bowl_volume_P',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='densitywetdry',
            name='bowl_weight_P',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='densitywetdry',
            name='layers',
            field=models.IntegerField(),
        ),
    ]
