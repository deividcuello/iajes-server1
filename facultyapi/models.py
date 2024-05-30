from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Faculty(models.Model):

  # title = models.CharField(max_length=255, default='')
  university = models.CharField(max_length=255, default='')
  email = models.CharField(max_length=255, default='')
  title = models.CharField(max_length=255, default='')
  country = models.CharField(max_length=255, default='')
  topics = models.TextField(default='')
  hidden = models.BooleanField(default=True)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
        return self.title