from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify

def upload_to_images(instance, filename):
    return 'resources/programs/images{filename}'.format(filename=filename)

class Center(models.Model):

  # title = models.CharField(max_length=255, default='')
  program_name = models.CharField(max_length=255, default='')
  email = models.CharField(max_length=255, default='')
  location = models.CharField(max_length=255, default='')
  center = models.CharField(max_length=255, default='')
  # director = models.CharField(max_length=255, default='')
  phone = models.CharField(max_length=255, default='')
  cover_url = models.ImageField(upload_to=upload_to_images, blank=True, null=True)
  hidden = models.BooleanField(default=True)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
        return self.title