# Generated by Django 5.0.3 on 2024-04-28 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='status',
            field=models.CharField(choices=[('NONE', 'Ninguno'), ('INTERNAL', 'Interno')], default='NONE', max_length=50),
        ),
    ]
