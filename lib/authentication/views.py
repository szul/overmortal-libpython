from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate 
from django.contrib.auth import login as system_login
from django.contrib.auth import logout as system_logout
from django.contrib.auth import load_backend
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from forms import *
import uuid

def join(request):
    if request.method == 'POST':
        form = UserForm(data = request.POST)
        if form.is_valid():
            new_user = form.save()
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
            if user.is_active:
                system_login(request, user)
                return HttpResponseRedirect(reverse(settings.AUTHENTICATION_JOIN_RETURN_STRING))
    else:
        form = UserForm()
    return render_to_response('register.html', locals())

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(data = request.POST)
        if form.is_valid():
            user = User.objects.get(email = form.cleaned_data['email'])
            if user:
                success = True
                temp_password = str(uuid.uuid1())
                user.set_password(temp_password)
                user.save()
                user.email_user('Password Reset from ' + settings.SITE_NAME, 'You are receiving this message before you indicated that you\'ve forgotten your password. You new temporary password is: ' + temp_password + '. Please log back into the web site and change your password.', from_email = settings.EMAIL_FROM)
            else:
                error = True
    else:
        form = ForgotPasswordForm()
    return render_to_response('forgot_password.html', locals())

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse(settings.AUTHENTICATION_LOGIN_RETURN_STRING))
    if request.GET and request.GET['next'] != None and request.GET['next'] != '':
        next = request.GET['next']
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        if form.is_valid():
            user = User.objects.get(email = form.cleaned_data['email'])
            user = authenticate(username = user.username, password = form.cleaned_data['password'])
            if user:
                system_login(request, user)
                if request.POST and request.POST['next'] != None and request.POST['next'] != '':
                    return HttpResponseRedirect(request.POST['next'])
                return HttpResponseRedirect(reverse(settings.AUTHENTICATION_LOGIN_RETURN_STRING))
            else:
                error = True
    else:
        form = LoginForm()
    return render_to_response('login.html', locals())

def logout(request):
    system_logout(request)
    return HttpResponseRedirect(reverse(settings.AUTHENTICATION_LOGOUT_RETURN_STRING))

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordForm(data = request.POST)
        if form.is_valid():
            success = True
            user = request.user
            user.set_password(form.cleaned_data['password1'])
            user.save()
    else:
        form = PasswordForm()
    return render_to_response('password.html', locals())
