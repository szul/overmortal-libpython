from django.conf.urls.defaults import *

urlpatterns = patterns(
    'overmortal.lib.authentication.openid.views',
    (r'complete/', 'complete'),
    (r'logout/', 'signout'),
    (r'login/', 'login'),
    (r'$', 'begin', { 'sreg':'email,nickname,fullname' }),
)
