# Generated by Django 2.2.5 on 2019-10-22 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='construction',
            name='start_day',
            field=models.DateField(),
        ),
    ]