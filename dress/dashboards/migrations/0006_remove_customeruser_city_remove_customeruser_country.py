# Generated by Django 5.2.3 on 2025-07-09 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0005_remove_customeruser_customer_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customeruser',
            name='city',
        ),
        migrations.RemoveField(
            model_name='customeruser',
            name='country',
        ),
    ]
