from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from overmortal.util.authentication.backend import load_django_backend, system_login
from overmortal.util.social import facebook
from models import Facebook
import uuid

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse(settings.FACEBOOK_LOGIN_RETURN_STRING))
    facebook_app_id = settings.FACEBOOK_APP_ID
    fb = facebook.Facebook(facebook_app_id)
    if(fb.init_data_from_cookie(request.COOKIES)):
        try:
            response = fb.get_user()
            if fb.error:
                del request.COOKIES['fbs_' + facebook_app_id]
            else:
                try:
                    fb_user = Facebook.objects.get(uid = response['id'])
                    user = User.objects.get(id = fb_user.user_id)
                    load_django_backend(user)
                    system_login(request, user)
                except ObjectDoesNotExist:
                    tmp = str(uuid.uuid1())
                    user = User.objects.create_user(username = 'fb' + response['id'], email = 'fb' + response['id'] + settings.FACEBOOK_DEFAULT_EMAIL_DOMAIN, password = tmp)
                    user.first_name = response['first_name']
                    user.last_name = response['last_name']
                    user.save()
                    fb_user = Facebook(user = user, uid = response['id'], first_name = response['first_name'], last_name = response['last_name'], web_site = response['website'], hometown = response['hometown']['name'])
                    fb_user.save()
                    load_django_backend(user)
                    system_login(request, user)
                return HttpResponseRedirect(reverse(settings.FACEBOOK_LOGIN_RETURN_STRING))
        except:
            del request.COOKIES['fbs_' + facebook_app_id]
    return render_to_response('facebook_login.html', locals())
