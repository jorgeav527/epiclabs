# Generated by Django 2.2.5 on 2020-06-26 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_material', '0003_densityvoids_name_element'),
    ]

    operations = [
        migrations.AddField(
            model_name='abssatucoeff',
            name='name_element',
            field=models.CharField(default='ladrillo', max_length=50),
            preserve_default=False,
        ),
    ]
