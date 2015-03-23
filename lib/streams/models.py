from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

MAX_ACTIVITY = 50

class Stream(models.Model):
    user = models.ForeignKey(User, unique = True)
    is_active = models.BooleanField(default = True)
    type_id = models.IntegerField();
    type = models.CharField(max_length = 255)
    title_html = models.TextField()
    content_html = models.TextField()
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)
    timestamp = models.TimeField(auto_now = True)
    def save(self):
        if settings.STREAMS_MAX_ACTIVITY:
            MAX_ACTIVITY = settings.STREAMS_MAX_ACTIVITY
        count = Stream.objects.count()
        if count > MAX_ACTIVITY:
            diff = count - MAX_ACTIVITY
            items = Stream.objects.all()[:diff]
            for item in items:
                item.delete()
        super(Stream, self).save()
