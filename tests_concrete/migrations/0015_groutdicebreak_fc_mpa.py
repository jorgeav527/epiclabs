# Generated by Django 2.2.5 on 2019-10-29 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_concrete', '0014_auto_20191029_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='groutdicebreak',
            name='fc_MPa',
            field=models.FloatField(editable=False, null=True),
        ),
    ]
