# Generated by Django 2.2.5 on 2019-10-21 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thesis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesis',
            name='line',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='start_day',
            field=models.DateField(),
        ),
    ]
