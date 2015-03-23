from django.contrib.sitemaps import Sitemap
from models import *

class Posts(Sitemap):
    changefreq = "never"
    priority = 0.5
    def items(self):
        return Post.objects.filter(is_draft = False)
    def lastmod(self, obj):
        return obj.date_created
