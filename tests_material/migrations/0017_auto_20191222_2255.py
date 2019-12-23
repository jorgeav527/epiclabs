# Generated by Django 2.2.5 on 2019-12-23 03:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_material', '0016_auto_20191222_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='masonrycompression',
            name='dilate',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='masonrycompression',
            name='done_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
