from django.conf.urls.defaults import *

urlpatterns = patterns('overmortal.components.flatfilepages.views',
    (r'^(?P<url>.*)$', 'flatfilepage'),
)
