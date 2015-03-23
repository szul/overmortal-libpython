from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Twitter(models.Model):
    user = models.ForeignKey(User, unique = True)
    is_active = models.BooleanField(default = True)
    username = models.CharField(max_length = 255)
    access_token = models.CharField(max_length = 255)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)
    timestamp = models.TimeField(auto_now = True)
