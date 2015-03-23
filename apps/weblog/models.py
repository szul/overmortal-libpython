from django.conf import settings
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import signals
from django.http import HttpResponseRedirect
from datetime import datetime
from tagging.models import Tag
from tagging.fields import TagField
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django_push.publisher import ping_hub
import re

MIME_TYPES = (
    ('audio/mpeg','audio/mpeg'),
    ('video/mp4','video/mp4'),
)

class Category(models.Model):
    name = models.CharField(max_length = 255)
    slug = models.CharField(max_length = 255)
    description = models.TextField(blank = True)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)
    timestamp = models.TimeField(auto_now = True)
    def __unicode__(self):
        return '%s' % self.name
    def get_absolute_url(self):
        return "/blog/category/%s/" % self.to_param()
    def to_param(self):
        return '%s-%s' % (self.id, re.sub(r'\W+','-',self.name.lower()))

class Post(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    byline = models.CharField(max_length = 255)
    title = models.CharField(max_length = 255)
    is_draft = models.BooleanField()
    content = models.TextField()
    tags = TagField()
    image_link = models.URLField(null = True, blank = True)
    media_link = models.URLField(null = True, blank = True)
    media_type = models.CharField(null = True, blank = True, max_length = 255, choices = MIME_TYPES)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)
    timestamp = models.TimeField(auto_now = True)
    def __unicode__(self):
        return '%s by %s' % (self.title, self.byline)
    def get_absolute_url(self):
        return "/blog/post/%s/" % self.to_param()
    def to_param(self):
        return '%s-%s' % (self.id, re.sub(r'\W+','-',self.title.lower()))
    def tagged_with(self):
        return Tag.objects.get_for_object(self)
 
def moderate_comments(instance, **kwargs):
    if not instance.id:
        post = Post.objects.get(id = instance.object_pk)
        delta = datetime.now() - post.date_created
        if delta.days > 30:
            instance.is_public = False

def notify_admin(instance, **kwargs):
    post = Post.objects.get(id = instance.object_pk)
    delta = datetime.now() - post.date_created
    if delta.days < 30 or instance.is_public:
        msg = EmailMessage('A new comment has been posted to ' + post.title, instance.comment + '<p>Follow the conversation here: <a href="' + settings.SITE_URL + post.get_absolute_url() + '">' + settings.SITE_URL + post.get_absolute_url() + '</a></p>', settings.WEBLOG_EMAIL_SENDER, [settings.WEBLOG_EMAIL_RECIPIENT])
        msg.content_subtype = 'html'
        msg.send()
        comments = Comment.objects.exclude(id = instance.id).filter(object_pk = post.id).order_by('user_email').values('user_email').distinct()
        for comment in comments:
            msg = EmailMessage('A new comment has been posted to ' + post.title, instance.comment + '<p>Follow the conversation here: <a href="' + settings.SITE_URL + post.get_absolute_url() + '">' + settings.SITE_URL + post.get_absolute_url() + '</a></p>', settings.WEBLOG_EMAIL_SENDER, [comment['user_email']])
            msg.content_subtype = 'html'
            msg.send()

def publish_to_hub(instance, **kwargs):
    post = Post.objects.get(id = instance.object_pk)
    ping_hub('http://%s%s' % (Site.objects.get_current(), post.get_absolute_url()))

signals.pre_save.connect(moderate_comments, sender=Comment)
signals.post_save.connect(notify_admin, sender=Comment)
signals.post_save.connect(publish_to_hub, sender=Post)
