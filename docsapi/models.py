from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify

def upload_to(instance, filename):
    return 'resources/docs/images{filename}'.format(filename=filename)


def upload_to_file(instance, filename):
    return 'images/docs/files{filename}'.format(filename=filename)


class Document(models.Model):

  title = models.CharField(max_length=255, default='')
#   cover_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
  document = models.FileField(blank=False, null=False, upload_to = upload_to_file) 
  year = models.CharField(max_length=255, default='')
  author = models.CharField(max_length=255, default='')
  hidden = models.BooleanField(default=True)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)

  
  def __str__(self):
        return self.title