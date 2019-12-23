# Generated by Django 2.2.5 on 2019-12-20 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests_concrete', '0038_auto_20191219_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='limedicebreak',
            name='construction',
        ),
        migrations.RemoveField(
            model_name='limedicebreak',
            name='course',
        ),
        migrations.RemoveField(
            model_name='limedicebreak',
            name='equipment',
        ),
        migrations.RemoveField(
            model_name='limedicebreak',
            name='reference_person',
        ),
        migrations.RemoveField(
            model_name='limedicebreak',
            name='tool',
        ),
        migrations.RemoveField(
            model_name='limedicebreak',
            name='user',
        ),
        migrations.RemoveField(
            model_name='limepicebreak',
            name='construction',
        ),
        migrations.RemoveField(
            model_name='limepicebreak',
            name='course',
        ),
        migrations.RemoveField(
            model_name='limepicebreak',
            name='equipment',
        ),
        migrations.RemoveField(
            model_name='limepicebreak',
            name='reference_person',
        ),
        migrations.RemoveField(
            model_name='limepicebreak',
            name='tool',
        ),
        migrations.RemoveField(
            model_name='limepicebreak',
            name='user',
        ),
        migrations.RemoveField(
            model_name='paverbreak',
            name='construction',
        ),
        migrations.RemoveField(
            model_name='paverbreak',
            name='course',
        ),
        migrations.RemoveField(
            model_name='paverbreak',
            name='equipment',
        ),
        migrations.RemoveField(
            model_name='paverbreak',
            name='reference_person',
        ),
        migrations.RemoveField(
            model_name='paverbreak',
            name='tool',
        ),
        migrations.RemoveField(
            model_name='paverbreak',
            name='user',
        ),
        migrations.DeleteModel(
            name='GroutDiceBreak',
        ),
        migrations.DeleteModel(
            name='LimeDiceBreak',
        ),
        migrations.DeleteModel(
            name='LimePiceBreak',
        ),
        migrations.DeleteModel(
            name='PaverBreak',
        ),
    ]
