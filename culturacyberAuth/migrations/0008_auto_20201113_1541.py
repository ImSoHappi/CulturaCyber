# Generated by Django 3.1.2 on 2020-11-13 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('culturacyberAuth', '0007_auto_20201113_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientmodel',
            name='description',
            field=models.TextField(max_length=100),
        ),
    ]
