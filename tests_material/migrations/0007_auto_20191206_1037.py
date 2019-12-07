# Generated by Django 2.2.5 on 2019-12-06 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_material', '0006_auto_20191205_2049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variationdimensions',
            name='n_d_high',
        ),
        migrations.RemoveField(
            model_name='variationdimensions',
            name='n_d_length',
        ),
        migrations.RemoveField(
            model_name='variationdimensions',
            name='n_d_width',
        ),
        migrations.AddField(
            model_name='bricktype',
            name='n_d_high',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bricktype',
            name='n_d_length',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bricktype',
            name='n_d_width',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
