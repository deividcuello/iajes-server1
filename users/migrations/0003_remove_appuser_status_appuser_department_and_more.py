# Generated by Django 5.0.3 on 2024-05-20 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_appuser_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='status',
        ),
        migrations.AddField(
            model_name='appuser',
            name='department',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='appuser',
            name='phone',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='appuser',
            name='university',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
