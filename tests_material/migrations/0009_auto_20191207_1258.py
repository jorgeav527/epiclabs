# Generated by Django 2.2.5 on 2019-12-07 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_material', '0008_parallelperpendicular_woodcompression'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parallelperpendicular',
            name='area_2',
            field=models.FloatField(editable=False),
        ),
        migrations.AlterField(
            model_name='parallelperpendicular',
            name='width_2',
            field=models.FloatField(),
        ),
    ]
