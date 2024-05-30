from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify

def upload_to(instance, filename):
    return 'images/projects/{filename}'.format(filename=filename)

class Project(models.Model):
  INDUSTRIES = (
       ('energy', 'Energy'),
       ('water', 'Water'),
       ('health', 'Health'),
       ('education', 'Education'),
       ('sustainable_construction', 'Sustainable Construction'),
       ('farming', 'Farming '),
    )
  REGIONS = (
       ('kircher', 'KIRCHER'),
       ('jheasa', 'JHEASA'),
       ('ausjal', 'AUSJAL'),
       ('ajcu-ap', 'AJCU-AP'),
       ('ajcu-am', 'AJCU-AM'),
       ('ajcu', 'AJCU'),
    )

  title = models.CharField(max_length=255, default='')
  image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
  college = models.CharField(max_length=255, default='')
  investigator = models.CharField(max_length=255, default='')
  start_year = models.CharField(max_length=255, default='')
  end_year = models.CharField(max_length=255, default='')
  isWorking = models.BooleanField(default=False)
  partner_organization = models.CharField(max_length=255, default='')
  keywords = models.TextField(default='')
  published_date = models.CharField(max_length=255, default='')
  region = models.CharField(max_length=50, choices=REGIONS, blank=False, null=False, default=REGIONS[0][0])
  industry = models.CharField(max_length=50, choices=INDUSTRIES, blank=False, null=False, default=INDUSTRIES[0][0])
  summary = models.TextField(default='')
  email = models.CharField(max_length=255, default='')
  hidden = models.BooleanField(default=True)
  approved = models.BooleanField(default=False)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)
  slug = models.SlugField(unique=True, default="", null=False)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank = True, null = True)
  
  def __str__(self):
        return self.title

  def save(self, *args, **kwargs):
      if not self.pk:
          self.slug = slugify(f'{self.title}-{str(self.created_at.date()).replace('-', '')}')
      super().save(*args, **kwargs)