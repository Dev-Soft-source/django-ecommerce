# Generated by Django 5.2.3 on 2025-07-10 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0008_remove_interfaceconfigures_file_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interfaceconfigures',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='interfaceconfigures',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='interfaceconfigures',
            name='media_content',
            field=models.FileField(default=1, upload_to='interface_media/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='interfaceconfigures',
            name='media_type',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='interfaceconfigures',
            name='small_title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='interfaceconfigures',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
