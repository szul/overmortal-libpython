from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from models import Profile
from forms import ProfileForm

def profile(request, username = None):
    api_key = settings.PEOPLE_GOOGLE_API_KEY
    show_profile_map = settings.PEOPLE_SHOW_PROFILE_MAP
    if username is None or username == '':
        return HttpResponseRedirect(reverse('overmortal.lib.people.views.dashboard'))
    else:
        user = User.objects.get(username = username)
        try:
            profile =  user.get_profile()
        except Exception:
            pass
    return render_to_response('profile.html', locals())

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(data = request.POST)
        if form.is_valid():
            form.user_id = request.user.id
            profile = form.save()
            return HttpResponseRedirect(reverse('overmortal.lib.people.views.dashboard'))
    else:
        try:
            profile = Profile.objects.get(user = request.user)
            data = {
                    'location': profile.location,
                    'web_site': profile.web_site,
                    'description': profile.description
                    }
            form = ProfileForm(data = data)
        except Exception:
            form = ProfileForm()
    return render_to_response('edit_profile.html', locals())

@login_required
def dashboard(request):
    return render_to_response('dashboard.html', locals())
