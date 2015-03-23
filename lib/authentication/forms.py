from django import forms
from django.contrib.auth.models import User

class UserForm(forms.Form):
    username = forms.CharField(max_length = 255)
    email = forms.EmailField()
    password1 = forms.CharField(max_length = 30, widget = forms.PasswordInput(render_value = False))
    password2 = forms.CharField(max_length = 30, widget = forms.PasswordInput(render_value = False))
    def clean_username(self):
    	try:
    		User.objects.get(username = self.cleaned_data['username'])
    		raise forms.ValidationError('This username is already in use. Please choose another.')
    	except User.DoesNotExist:
    		pass
    	return self.cleaned_data['username']
    def clean_email(self):
        try:
            User.objects.get(email = self.cleaned_data['email'])
            raise forms.ValidationError('This email is already in use. Please choose another.')
        except User.DoesNotExist:
            pass
        return self.cleaned_data['email']
    def clean(self):
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError('Your password and password confirmation must match.')
		return self.cleaned_data
    def save(self):
		new_user = User.objects.create_user(username = self.cleaned_data['username'], email = self.cleaned_data['email'], password = self.cleaned_data['password1'])
		return new_user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length = 30, widget = forms.PasswordInput(render_value = False))

class PasswordForm(forms.Form):
    password1 = forms.CharField(max_length = 30, widget = forms.PasswordInput(render_value = False))
    password2 = forms.CharField(max_length = 30, widget = forms.PasswordInput(render_value = False))
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError('Your password and password confirmation must match.')
        return self.cleaned_data

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
