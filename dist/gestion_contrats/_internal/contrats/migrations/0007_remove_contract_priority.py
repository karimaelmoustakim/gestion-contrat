# Generated by Django 5.0.6 on 2024-07-23 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contrats', '0006_contract_priority'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='priority',
        ),
    ]
