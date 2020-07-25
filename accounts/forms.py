from django import forms
from django.contrib.auth import get_user_model
from django.forms.utils import ErrorList
from django.utils import timezone

from .models import Profile

USER = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'john_doe@yourdomain.com'
    }))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())


class Registration(forms.Form):
    username = forms.CharField(max_length=150,
                               required=True,
                               help_text='Required: Might include a-zA-Z_.1-9',
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'the_undisputed12',
                               }))
    email = forms.EmailField(max_length=150,
                             required=True,
                             help_text='Required',
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'joe_smith@domain.com',
                             }))
    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Joe'
                                 }))
    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Smith'
                                }))
    password1 = forms.CharField(max_length=150, widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password'
            }
    ))
    password2 = forms.CharField(max_length=150, widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password'
            }
    ))

    profile_img = forms.ImageField()

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 != password1:
            self._errors['password2'] = ErrorList([u'Password do not match!'])

        return self.cleaned_data

    @staticmethod
    def save(data):
        u = USER()
        u.first_name = data['first_name']
        u.last_name = data['last_name']
        u.username = data['username']
        u.email = data['email']
        u.set_password(data['password1'])
        # make this false when activating email verification
        u.is_active = True
        u.save()

        profile = Profile()
        profile.user = u
        profile.profile_img = data['profile_img']
        profile.activation_key = data['activation_key']
        profile.key_expires_at = timezone.now() + timezone.timedelta(days=2)
        profile.save()
        return u



