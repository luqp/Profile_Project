import glob
import random

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate, login, logout, 
                                 update_session_auth_hash)
from . import forms


def select_user_img(user):
    try:
        path = user.avatar.url
    except ValueError:
        path = select_ramdon_image()
    return path


def select_ramdon_image():
    url_images = []
    for path in glob.glob('media/imgs/*.svg'):
        path = '/' + path
        url_images.append(path)
    url = random.choice(url_images)
    return url


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('accounts:profile_detail'))
                else:
                    messages.error(
                        request,
                        "That user account has been disabled"
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = forms.UserCreationForm()
    if request.method == 'POST':
        form = forms.UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('accounts:profile_detail'))
    return render(request, 'accounts/sign_up.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile_detail(request):
    user = request.user
    path = select_user_img(user)
    return render(request, 'accounts/profile_detail.html', {
        'user': user,
        'path': path,
    })


@login_required
def profile_edit(request):
    user = request.user
    form = forms.ProfileForm(instance=user)
    if request.method == 'POST':
        form = forms.ProfileForm(
            instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "You saved successful your data"
            )
            return HttpResponseRedirect(reverse('accounts:profile_detail'))
    path = select_user_img(user)
    return render(request, 'accounts/profile_form.html', {
        'form': form,
        'title': 'Edit Profile',
        'path': path,
    })


@login_required
def change_password(request):
    user = request.user
    form = forms.CustomPasswordChangeForm(user)
    if request.method == 'POST':
        form = forms.CustomPasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('accounts:profile_detail'))
        else:
            messages.error(request, 'Please correct the error below.')
    path = select_user_img(user)
    return render(request, 'accounts/password_form.html', {
        'form': form,
        'title': 'Change password',
        'path': path,
    })
