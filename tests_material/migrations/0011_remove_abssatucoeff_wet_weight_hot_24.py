# Generated by Django 2.2.5 on 2019-12-11 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests_material', '0010_auto_20191207_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abssatucoeff',
            name='wet_weight_hot_24',
        ),
    ]