import hashlib

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.views import View
from .forms import LoginForm, Registration

# Create your views here.
USER = get_user_model()


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))
        return render(request, self.template_name, context={'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse('accounts:login'))


def generate_activation_key(username):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(20, chars)
    return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()


class SignUpView(View):
    template_name = 'accounts/signup.html'
    form_class = Registration

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            data = form.cleaned_data
            data['activation_key'] = generate_activation_key(
                    form.cleaned_data['username'])

            form.save(data)
            return redirect(reverse('home'))
        return render(request, self.template_name, context={'form': form})


@login_required
def profile_view(request, pk):
    user = USER.objects.get(pk=pk)
    return render(request, 'accounts/profile.html', {'user': user})
