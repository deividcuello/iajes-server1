# Generated by Django 5.0.3 on 2024-05-19 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facultyapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='topics',
            field=models.TextField(default=''),
        ),
    ]