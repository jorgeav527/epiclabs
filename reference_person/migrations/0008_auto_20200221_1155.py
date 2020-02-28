# Generated by Django 2.2.5 on 2020-02-21 16:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reference_person', '0007_auto_20191023_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='referenceperson',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='referenceperson',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
