# Generated by Django 2.2.5 on 2019-12-12 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_material', '0013_auto_20191211_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warping',
            name='downface_concave',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='warping',
            name='downface_convex',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='warping',
            name='upface_concave',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='warping',
            name='upface_convex',
            field=models.FloatField(default=0),
        ),
    ]
