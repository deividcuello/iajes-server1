from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify

def upload_to_images(instance, filename):
    return 'images/news/{filename}'.format(filename=filename)

class News(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    image_url = models.ImageField(upload_to=upload_to_images, blank=True, null=True)
    description = models.TextField()
    hidden = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, default="", null=False)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank = True, null = True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(f'{self.title}-{str(self.created_at.date()).replace('-', '')}')
        super().save(*args, **kwargs)

        