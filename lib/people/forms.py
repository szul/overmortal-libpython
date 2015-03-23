from django import forms
from django.contrib.auth.models import User
from models import Profile

class ProfileForm(forms.Form):
	location = forms.CharField(widget=forms.TextInput)
	web_site = forms.URLField(widget=forms.TextInput, verify_exists = True)
	description = forms.CharField(widget=forms.Textarea)
	user_id = None
	def save(self):
		user = User.objects.get(id = self.user_id)
		try:
			profile = Profile.objects.get(user = user)
			profile.location = self.cleaned_data['location']
			profile.web_site = self.cleaned_data['web_site']
			profile.description = self.cleaned_data['description']
		except Exception:
			profile = Profile(user = user, location = self.cleaned_data['location'], web_site = self.cleaned_data['web_site'], description = self.cleaned_data['description'])
		profile.save()
		return profile
