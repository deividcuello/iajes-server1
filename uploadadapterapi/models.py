from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

def upload_to(instance, filename):
    return 'images/adapter/{filename}'.format(filename=filename)

class UploadAdapter(models.Model):
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.SET_NULL, blank = True, null = True)