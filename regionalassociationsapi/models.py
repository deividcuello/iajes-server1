from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class RegionalAssociation(models.Model):
    REGIONS = (
       ('kircher', 'KIRCHER'),
       ('jheasa', 'JHEASA'),
       ('ausjal', 'AUSJAL'),
       ('ajcu-ap', 'AJCU-AP'),
       ('ajcu-am', 'AJCU-AM'),
       ('ajcu', 'AJCU'),
    )

    video_url = models.URLField(max_length=200)
    title = models.CharField(max_length=255, default='')
    region = models.CharField(max_length=50, choices=REGIONS, blank=False, null=False, default=REGIONS[0][0])
    hidden = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

        

