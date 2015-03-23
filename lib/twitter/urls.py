from django.conf.urls.defaults import *

urlpatterns = patterns(
    'overmortal.lib.twitter.views',
    (r'^connect/', 'connect'),
    (r'^oauth-request/', 'oauth_request'),
    (r'^oauth-return/', 'oauth_return'),
)
