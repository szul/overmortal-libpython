from django.conf.urls.defaults import *

urlpatterns = patterns(
    'overmortal.lib.people.views',
    (r'^edit-profile/', 'edit_profile'),
    (r'^dashboard/', 'dashboard'),
    (r'^(?P<username>\w*)$', 'profile'),
)
