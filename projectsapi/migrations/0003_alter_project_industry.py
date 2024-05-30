# Generated by Django 5.0.3 on 2024-04-04 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectsapi', '0002_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='industry',
            field=models.CharField(choices=[('energy', 'Energy'), ('water', 'Water'), ('health', 'Health'), ('education', 'Education'), ('sustainable_construction', 'Sustainable Construction'), ('farming', 'Farming ')], default='energy', max_length=50),
        ),
    ]
