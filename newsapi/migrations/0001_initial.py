# Generated by Django 5.0.3 on 2024-04-05 13:55

import django.utils.timezone
import newsapi.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image_url', models.ImageField(blank=True, null=True, upload_to=newsapi.models.upload_to_images)),
                ('description', models.TextField()),
                ('hidden', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(default='', unique=True)),
            ],
        ),
    ]
