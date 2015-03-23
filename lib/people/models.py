from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from overmortal.util.geocoding import google

class Profile(models.Model):
    user = models.ForeignKey(User, unique = True)
    is_active = models.BooleanField(default = True)
    location = models.CharField(max_length = 255, null = True)
    latitude = models.CharField(max_length = 255, null = True)
    longitude = models.CharField(max_length = 255, null = True)
    web_site = models.URLField(null = True)
    description = models.TextField(null = True)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)
    timestamp = models.TimeField(auto_now = True)
    def save(self, *args, **kwargs):
        if self.location:
            if settings.PEOPLE_USE_GEOCODING and settings.PEOPLE_GOOGLE_API_KEY:
                geocoder = google.Geocoder(settings.PEOPLE_GOOGLE_API_KEY)
                count = geocoder.query(self.location)
                if geocoder.longitude != None and geocoder.latitude != None:
                    self.longitude = geocoder.longitude
                    self.latitude = geocoder.latitude
        super(Profile, self).save(*args, **kwargs)
