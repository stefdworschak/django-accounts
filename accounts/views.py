#!/usr/bin/env python
from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse

from accounts.helpers import lang_choices_as_dict
from accounts.forms import (UserLoginForm, UserRegistrationForm,
                            CustomChangePasswordForm,
                            CustomLoggedinUserChangeForm)
from accounts.models import CustomUser

LOGIN_REDIRECT = settings.LOGIN_REDIRECT


def register(request):
    """ Page to create a new user account """
    if request.user.is_authenticated:
        return redirect(reverse(LOGIN_REDIRECT))
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            user = registration_form.save()

            user = auth.authenticate(username=request.POST.get('username'),
                                     password=request.POST.get('password1'))
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in!")
                return redirect(reverse(LOGIN_REDIRECT))
            else:
                messages.error(request,
                               'Username and password combination is wrong.')
        else:
            for e in registration_form.errors.values():
                messages.error(request, e)
    else:
        registration_form = UserRegistrationForm()

    return render(request, 'registration.html',
                  {'registration_form': registration_form})


def login(request):
    """ Page to log in to an existing user account """
    if request.user.is_authenticated:
        return redirect(reverse(LOGIN_REDIRECT))

    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST.get('username'),
                                     password=request.POST.get('password'))
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in!")
                return redirect(reverse(LOGIN_REDIRECT))
            else:
                messages.error(request,
                               'Username and password combination is wrong.')
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})


#@login_required
def change_password(request):
    if request.method == 'POST':
        change_password_form = CustomChangePasswordForm(request.POST)

        if change_password_form.is_valid():
            user = auth.authenticate(
                username=request.user.username,
                password=request.POST.get('current_password'))

            if (request.POST.get('new_password1')
                    == request.POST.get('new_password2')):
                user.set_password(request.POST.get('new_password1'))
            else:
                messages.error(
                    request,
                    'New password and Confirm Password were not the same value.')  # noqa: E501
        else:
            messages.error(request,
                           'Username and password combination is wrong.')

    else:
        change_password_form = CustomChangePasswordForm()
    return render(request, 'change_password.html',
                  {'change_password_form': change_password_form})


@login_required
def user_account(request):
    """ Shows a basic user account page """
    if request.method == 'POST':
        change_user_form = CustomLoggedinUserChangeForm(request.POST)
        if change_user_form.is_valid():
            user = CustomUser.objects.filter(id=request.user.id)
            if user:
                user.update(
                    email=request.POST.get('email'),
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    language=request.POST.get('language'))
                messages.success(request, 'Account updated successfully.')
            else:
                messages.error(request,
                               'An unexpected error occurred: Logged in user not found')  # noqa: E501
        else:
            messages.error(request,
                           'Username and password combination is wrong.')
    else:
        change_user_form = CustomLoggedinUserChangeForm(instance=request.user)
    return render(request, 'user_account.html',
                  {
                    'lang_choices': lang_choices_as_dict(),
                    'change_user_form': change_user_form
                  })

@login_required
def upload_image(request):
    return redirect(reverse('account'))


@login_required
def logout(request):
    """ Log user out """
    auth.logout(request)
    messages.success(request, "You have been logged out!")
    return redirect(reverse('login'))


@login_required
def testpage(request):
    """ Page to test that the login worked """
    return render(request, 'testpage.html')


def handler404(request, exception):
    """ Redirect to the index page if page is not found """
    return redirect(reverse('login'))
