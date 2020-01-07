# Generated by Django 2.2.5 on 2020-01-07 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_soil', '0022_globalmesh'),
    ]

    operations = [
        migrations.RenameField(
            model_name='globalmesh',
            old_name='tamiz_10',
            new_name='tamiz_N_10',
        ),
        migrations.RenameField(
            model_name='globalmesh',
            old_name='tamiz_100',
            new_name='tamiz_N_100',
        ),
        migrations.RenameField(
            model_name='globalmesh',
            old_name='tamiz_140',
            new_name='tamiz_N_140',
        ),
        migrations.RenameField(
            model_name='globalmesh',
            old_name='tamiz_16',
            new_name='tamiz_N_16',
        ),
        migrations.RenameField(
            model_name='globalmesh',
            old_name='tamiz_20',
            new_name='tamiz_N_20',
        ),
        migrations.RenameField(
            model_name='globalmesh',
            old_name='tamiz_200',
            new_name='tamiz_N_200',
        ),
        migrations.RenameField(
            model_name='globalmesh',
            old_name='tamiz_30',
            new_name='tamiz_N_30',
        ),
        migrations.RenameField(
            model_name='globalmesh',
            old_name='tamiz_40',
            new_name='tamiz_N_4',
        ),
        migrations.RenameField(
            model_name='globalmesh',
            old_name='tamiz_50',
            new_name='tamiz_N_40',
        ),
        migrations.RenameField(
            model_name='globalmesh',
            old_name='tamiz_60',
            new_name='tamiz_N_50',
        ),
        migrations.RenameField(
            model_name='globalmesh',
            old_name='tamiz_8',
            new_name='tamiz_N_60',
        ),
        migrations.RenameField(
            model_name='globalmesh',
            old_name='tamiz_80',
            new_name='tamiz_N_8',
        ),
        migrations.AddField(
            model_name='globalmesh',
            name='tamiz_N_80',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
