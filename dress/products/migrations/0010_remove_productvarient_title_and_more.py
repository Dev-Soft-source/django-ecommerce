# Generated by Django 5.2.3 on 2025-07-09 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_productvarient_badge_id_productvarient_color_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvarient',
            name='title',
        ),
        migrations.AddField(
            model_name='productvarient',
            name='product_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.products'),
            preserve_default=False,
        ),
    ]
