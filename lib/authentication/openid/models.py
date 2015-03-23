from django.db import models
from django.contrib.auth.models import User

class Nonce(models.Model):
    nonce = models.CharField(max_length = 8)
    expires = models.IntegerField()
    def __str__(self):
        return "Nonce: %s" % self.nonce

class Association(models.Model):
    server_url = models.TextField(max_length = 2047)
    handle = models.CharField(max_length = 255)
    secret = models.TextField(max_length = 255) # Stored base64 encoded
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.TextField(max_length = 64)
    def __str__(self):
        return "Association: %s, %s" % (self.server_url, self.handle)

class Openid(models.Model):
    user = models.ForeignKey(User)
    is_active = models.BooleanField(default = True)
    url = models.URLField(max_length = 255)
    nickname = models.CharField(max_length = 255, null = True)
    email = models.EmailField(max_length = 255, null = True)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)
    timestamp = models.TimeField(auto_now = True)
