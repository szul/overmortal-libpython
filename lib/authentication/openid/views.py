from django.http import HttpResponse, HttpResponseRedirect, get_host
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.conf import settings
from models import Openid as OpenIDModel
from overmortal.util.authentication.backend import load_django_backend, system_login
import uuid

import md5, re, time, urllib
from openid.consumer.consumer import Consumer, \
    SUCCESS, CANCEL, FAILURE, SETUP_NEEDED
from openid.consumer.discover import DiscoveryFailure
from yadis import xri

from util import OpenID, DjangoOpenIDStore, from_openid_response

from django.utils.html import escape

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse(settings.AUTHENTICATION_OPENID_LOGIN_RETURN_STRING))
    if request.openid:
        try:
            openid = OpenIDModel.objects.get(url = request.openid)
            user = User.objects.get(id = openid.user_id)
            load_django_backend(user)
            system_login(request, user)
            return HttpResponseRedirect(reverse(settings.AUTHENTICATION_OPENID_LOGIN_RETURN_STRING))
        except:
            tmp = str(uuid.uuid1())
            nickname = request.openid.sreg['nickname'] or request.openid
            email = request.openid.sreg['email'] or 'openid' + tmp + settings.AUTHENTICATION_OPENID_DEFAULT_EMAIL_DOMAIN
            user = None
            try:
                user = User.objects.create_user(username = nickname, email = email, password = tmp)
            except IntegrityError:
                p = re.compile('@|\.', re.VERBOSE)
                email = p.sub('', email)
                user = User.objects.create_user(username = email, email = email, password = tmp)
            oi = OpenIDModel(user = user, url = request.openid, nickname = nickname, email = email)
            oi.save()
            load_django_backend(user)
            system_login(request, user)
            return HttpResponseRedirect(reverse(settings.AUTHENTICATION_OPENID_LOGIN_RETURN_STRING))
    else:
        return HttpResponseRedirect(reverse('overmortal.lib.authentication.openid.views.begin'))

def get_url_host(request):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    host = escape(get_host(request))
    return '%s://%s' % (protocol, host)

def get_full_url(request):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    host = escape(request.META['HTTP_HOST'])
    return get_url_host(request) + request.get_full_path()

next_url_re = re.compile('^/[-\w/]+$')

def is_valid_next_url(next):
    # When we allow this:
    #   /openid/?next=/welcome/
    # For security reasons we want to restrict the next= bit to being a local 
    # path, not a complete URL.
    return bool(next_url_re.match(next))

def begin(request, sreg=None, extension_args=None, redirect_to=None, 
        on_failure=None):
    
    on_failure = on_failure or default_on_failure
    
    if request.GET.get('logo'):
        # Makes for a better demo
        return logo(request)
    
    extension_args = extension_args or {}
    if sreg:
        extension_args['sreg.optional'] = sreg
    trust_root = getattr(
        settings, 'AUTHENTICATION_OPENID_TRUST_ROOT', get_url_host(request) + '/'
    )
    redirect_to = redirect_to or getattr(
        settings, 'AUTHENTICATION_OPENID_REDIRECT_TO',
        # If not explicitly set, assume current URL with complete/ appended
        get_full_url(request).split('?')[0] + 'complete/'
    )
    # In case they were lazy...
    if not redirect_to.startswith('http://'):
        redirect_to =  get_url_host(request) + redirect_to
    
    if request.GET.get('next') and is_valid_next_url(request.GET['next']):
        if '?' in redirect_to:
            join = '&'
        else:
            join = '?'
        redirect_to += join + urllib.urlencode({
            'next': request.GET['next']
        })
    
    user_url = request.POST.get('openid_url', None)
    if not user_url:
        request_path = request.path
        if request.GET.get('next'):
            request_path += '?' + urllib.urlencode({
                'next': request.GET['next']
            })
        
        return render('signin.html', {
            'action': request_path,
            'logo': request.path + '?logo=1',
        })
    
    if xri.identifierScheme(user_url) == 'XRI' and getattr(
        settings, 'AUTHENTICATION_OPENID_DISALLOW_INAMES', False
        ):
        return on_failure(request, 'i-names are not supported')
    
    consumer = Consumer(request.session, DjangoOpenIDStore())
    try:
        auth_request = consumer.begin(user_url)
    except DiscoveryFailure:
        return on_failure(request, "The OpenID was invalid")
    
    # Add extension args (for things like simple registration)
    for name, value in extension_args.items():
        namespace, key = name.split('.', 1)
        auth_request.addExtensionArg(namespace, key, value)
    
    redirect_url = auth_request.redirectURL(trust_root, redirect_to)
    return HttpResponseRedirect(redirect_url)

def complete(request, on_success=None, on_failure=None):
    on_success = on_success or default_on_success
    on_failure = on_failure or default_on_failure
    
    consumer = Consumer(request.session, DjangoOpenIDStore())
    openid_response = consumer.complete(dict(request.GET.items()))
    
    if openid_response.status == SUCCESS:
        return on_success(request, openid_response.identity_url, openid_response)
    elif openid_response.status == CANCEL:
        return on_failure(request, 'The request was cancelled')
    elif openid_response.status == FAILURE:
        return on_failure(request, openid_response.message)
    elif openid_response.status == SETUP_NEEDED:
        return on_failure(request, 'Setup needed')
    else:
        assert False, "Bad openid status: %s" % openid_response.status

def default_on_success(request, identity_url, openid_response):
    if 'openids' not in request.session.keys():
        request.session['openids'] = []
    
    # Eliminate any duplicates
    request.session['openids'] = [
        o for o in request.session['openids'] if o.openid != identity_url
    ]
    request.session['openids'].append(from_openid_response(openid_response))
    
    next = request.GET.get('next', '').strip()
    if not next or not is_valid_next_url(next):
        next = getattr(settings, 'AUTHENTICATION_OPENID_REDIRECT_NEXT', '/')
    
    return HttpResponseRedirect(next)

def default_on_failure(request, message):
    return render('failure.html', {
        'message': message
    })

def signout(request):
    request.session['openids'] = []
    next = request.GET.get('next', '/')
    if not is_valid_next_url(next):
        next = '/'
    return HttpResponseRedirect(next)

def logo(request):
    return HttpResponse(
        OPENID_LOGO_BASE_64.decode('base64'), mimetype='image/gif'
    )

# Logo from http://openid.net/login-bg.gif
# Embedded here for convenience; you should serve this as a static file
OPENID_LOGO_BASE_64 = """
R0lGODlhEAAQAMQAAO3t7eHh4srKyvz8/P5pDP9rENLS0v/28P/17tXV1dHEvPDw8M3Nzfn5+d3d
3f5jA97Syvnv6MfLzcfHx/1mCPx4Kc/S1Pf189C+tP+xgv/k1N3OxfHy9NLV1/39/f///yH5BAAA
AAAALAAAAAAQABAAAAVq4CeOZGme6KhlSDoexdO6H0IUR+otwUYRkMDCUwIYJhLFTyGZJACAwQcg
EAQ4kVuEE2AIGAOPQQAQwXCfS8KQGAwMjIYIUSi03B7iJ+AcnmclHg4TAh0QDzIpCw4WGBUZeikD
Fzk0lpcjIQA7
"""
