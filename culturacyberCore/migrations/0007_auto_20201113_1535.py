# Generated by Django 3.1.2 on 2020-11-13 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('culturacyberCore', '0006_auto_20201112_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitymodel',
            name='description',
            field=models.TextField(max_length=400),
        ),
    ]
