from django.conf.urls.defaults import *

urlpatterns = patterns(
    'overmortal.lib.facebook.views',
    (r'login/', 'login'),
#    (r'connect/', 'connect'),
)
