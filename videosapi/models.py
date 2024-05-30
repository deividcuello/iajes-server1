from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify

class Video(models.Model):
    # video_url = models.ImageField(upload_to=upload_to_images, blank=True, null=True)
    video_url = models.URLField(max_length=200)
    title = models.CharField(max_length=255, default='')
    hidden = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank = True, null = True)
    
    def __str__(self):
        return self.title

        