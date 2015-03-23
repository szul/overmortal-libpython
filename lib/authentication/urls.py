from django.conf.urls.defaults import *

urlpatterns = patterns(
    'overmortal.lib.authentication.views',
    (r'^join/', 'join'),
    (r'^login/', 'login'),
    (r'^logout/', 'logout'),
    (r'forgot-password/$', 'forgot_password'),
    (r'password/$', 'change_password'),
)
