# Generated by Django 2.2.5 on 2019-10-19 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course',
            field=models.CharField(max_length=50),
        ),
    ]
