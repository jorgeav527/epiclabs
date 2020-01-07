# Generated by Django 2.2.5 on 2020-01-05 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_soil', '0020_auto_20191126_2323'),
    ]

    operations = [
        migrations.RenameField(
            model_name='granulometricglobal',
            old_name='tamiz_1',
            new_name='hygr_humid',
        ),
        migrations.RemoveField(
            model_name='granulometricglobal',
            name='tamiz_10',
        ),
        migrations.RemoveField(
            model_name='granulometricglobal',
            name='tamiz_100',
        ),
        migrations.RemoveField(
            model_name='granulometricglobal',
            name='tamiz_1_1o2',
        ),
        migrations.RemoveField(
            model_name='granulometricglobal',
            name='tamiz_1o2',
        ),
        migrations.RemoveField(
            model_name='granulometricglobal',
            name='tamiz_20',
        ),
        migrations.RemoveField(
            model_name='granulometricglobal',
            name='tamiz_200',
        ),
        migrations.RemoveField(
            model_name='granulometricglobal',
            name='tamiz_3o4',
        ),
        migrations.RemoveField(
            model_name='granulometricglobal',
            name='tamiz_3o8',
        ),
        migrations.RemoveField(
            model_name='granulometricglobal',
            name='tamiz_4',
        ),
        migrations.RemoveField(
            model_name='granulometricglobal',
            name='tamiz_40',
        ),
        migrations.RemoveField(
            model_name='granulometricglobal',
            name='tamiz_60',
        ),
        migrations.RemoveField(
            model_name='granulometricglobal',
            name='tamiz_fondo',
        ),
        migrations.AddField(
            model_name='granulometricglobal',
            name='liquid_limit',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='granulometricglobal',
            name='max_size',
            field=models.CharField(choices=[('4"', '4 inch'), ('3"', '3 inch'), ('2 1/2"', '2 1/2 inch'), ('2"', '2 inch'), ('1 1/2"', '1 1/2 inch'), ('1"', '1 inch'), ('3/4"', '3/4 inch'), ('1/2"', '1/2 inch'), ('3/8"', '3/8 inch')], default='2"', max_length=7),
        ),
        migrations.AddField(
            model_name='granulometricglobal',
            name='organic',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='granulometricglobal',
            name='plastic_index',
            field=models.FloatField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='granulometricglobal',
            name='plastic_limit',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
