# Generated by Django 3.1.2 on 2020-11-11 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('culturacyberAuth', '0004_auto_20201111_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermodel',
            old_name='cultureteam',
            new_name='is_cultureteam',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='organizer',
            new_name='is_organizer',
        ),
    ]