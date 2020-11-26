# Generated by Django 3.1.3 on 2020-11-26 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('culturacyberAuth', '0011_remove_usermodel_email'),
        ('culturacyberCore', '0011_auto_20201126_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='client_module_model',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='culturacyberAuth.clientmodel'),
        ),
        migrations.AddField(
            model_name='client_module_model',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='culturacyberCore.modulemodel'),
        ),
        migrations.AddField(
            model_name='modulemodel',
            name='client',
            field=models.ManyToManyField(blank=True, through='culturacyberCore.client_module_Model', to='culturacyberAuth.clientModel'),
        ),
    ]
