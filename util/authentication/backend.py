from django.contrib.auth import login, load_backend
from django.conf import settings

def load_django_backend(user):
	if not hasattr(user, 'backend'):
	        for backend in settings.AUTHENTICATION_BACKENDS:
	            if user == load_backend(backend).get_user(user.pk):
	                user.backend = backend
	                break

def system_login(request, user):
	if hasattr(user, 'backend'):
		login(request, user)
	else:
		raise Exception('Loading of backend authentication failed.')
