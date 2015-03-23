from django.contrib.syndication.feeds import Feed
from django_push.publisher.feeds import Feed as Push
from django.conf import settings
from models import Post

class Rss(Feed):
    title = settings.WEBLOG_TITLE
    link = "/"
    description = settings.WEBLOG_DESC
    def items(self):
        return Post.objects.filter(is_draft = False).order_by('-date_created')[:25]
    def item_pubdate(self, item):
        return item.date_created

class Atom(Push):
    title = settings.WEBLOG_TITLE
    link = "/"
    subtitle = settings.WEBLOG_DESC
    def items(self):
        return Post.objects.filter(is_draft = False).order_by('-date_created')[:25]
    def item_description(self, item):
        return item.content
    def item_pubdate(self, item):
        return item.date_created
