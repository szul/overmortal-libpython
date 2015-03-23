from django.conf.urls.defaults import *
from feeds import *

feeds = {
  'rss': Rss,
  'atom': Atom,
}

urlpatterns = patterns('',
  (r'^category/(?P<category_slug>.+)/$', 'overmortal.apps.weblog.views.blog'),
  (r'^category/(?P<category_slug>.+)/page/(?P<page>\d+)/$', 'overmortal.apps.weblog.views.blog'),
  (r'^page/(?P<page>\d+)/$', 'overmortal.apps.weblog.views.blog'),
  (r'^post/(?P<post_id>\w+)', 'overmortal.apps.weblog.views.post'),
  (r'^tag/(?P<tag>[\w\s]+)/page/(?P<page>\d+)/$', 'overmortal.apps.weblog.views.tag'),
  (r'^tag/(?P<tag>[\w\s]+)/$', 'overmortal.apps.weblog.views.tag'),
  (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
  (r'^metaweblog/', 'overmortal.apps.weblog.xmlrpc.view', {'module':'overmortal.apps.weblog.metaweblog'}),
  (r'^comments/post/', 'overmortal.apps.weblog.views.override_post_comment'),
  (r'^comments/', include('django.contrib.comments.urls')),
  (r'^admin/$', 'overmortal.apps.weblog.admin.blog'),
  (r'^admin/page/(?P<page>\d+)/$', 'overmortal.apps.weblog.admin.blog'),
  (r'^admin/post/delete/(?P<post_id>\w+)', 'overmortal.apps.weblog.admin.delete_post'),
  (r'^admin/post/(?P<post_id>\w+)*', 'overmortal.apps.weblog.admin.post'),
  (r'^admin/categories/$', 'overmortal.apps.weblog.admin.categories'),
  (r'^admin/category/delete/(?P<category_id>\w+)', 'overmortal.apps.weblog.admin.delete_category'),
  (r'^admin/category/(?P<category_id>\w+)*', 'overmortal.apps.weblog.admin.category'),
  (r'^$', 'overmortal.apps.weblog.views.blog'),
)
