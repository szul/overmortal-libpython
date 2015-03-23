from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Facebook(models.Model):
    user = models.ForeignKey(User, unique = True)
    is_active = models.BooleanField(default = True)
    uid = models.CharField(max_length = 255)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    web_site = models.CharField(max_length = 255, null = True)
    hometown = models.CharField(max_length = 255, null = True)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)
    timestamp = models.TimeField(auto_now = True)
