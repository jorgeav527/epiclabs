# Generated by Django 2.2.5 on 2019-09-28 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_material', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groutdicebreak',
            name='edad',
            field=models.IntegerField(editable=False),
        ),
    ]
