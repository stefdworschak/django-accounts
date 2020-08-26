import re

from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import (UserCreationForm,
                                       PasswordResetForm, SetPasswordForm,
                                       UserChangeForm)
from django.core.exceptions import ValidationError

from .models import CustomUser, LANG_CHOICES

PATTERN = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[\w~@#$%^&*+=`|{}:;!.?\"()\[\]\-\[/\]]{8,}$'  # noqa: E501


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)


class UserLoginForm(forms.Form):
    """ Form to handle login """
    email = forms.CharField(widget=forms.TextInput(
                               attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
                               attrs={'class': 'form-control'}))


class UserRegistrationForm(UserCreationForm):
    """ Form to handle user registration """
    email = forms.EmailField(widget=forms.TextInput(
                                attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
                                attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
                                attrs={'class': 'form-control'}))
    language = forms.CharField(widget=forms.Select(
                               choices=LANG_CHOICES,
                               attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = email

        if CustomUser.objects.filter(email=email).exclude(username=username):
            raise ValidationError(u"Email Addres must be unique")
        return email

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 or not password2:
            raise ValidationError(u"One or both password fields empty")

        if password1 != password2:
            raise ValidationError(u"Passwords do not match")
        return password2


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.TextInput(
                             attrs={'class': 'form-control'}))


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}))


class CustomChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(
                                       attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}))

    def clean_password(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        current_password = self.cleaned_data.get('current_password')
        if not new_password1 or not new_password2 or not current_password:
            raise ValidationError(u"One or both password fields empty")

        if new_password1 != new_password2:
            raise ValidationError(u"Passwords do not match")

        if not bool(re.fullmatch(PATTERN, new_password2)):
            raise ValidationError(
                ("The new password does not meet the required complexity. "
                 "You need at least one lowercase, one uppercase letter, one "
                 "number and one special character."))
        else:
            print("New Pass: ", new_password2)
        return new_password2


class CustomLoggedinUserChangeForm(UserChangeForm):
    email = forms.EmailField(widget=forms.TextInput(
                                attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control'}),
                                required=False)
    last_name = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control'}),
                                required=False)
    language = forms.CharField(widget=forms.Select(
                               choices=LANG_CHOICES,
                               attrs={'class': 'form-control'}),
                               required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = email
        if CustomUser.objects.filter(email=email).exclude(username=username):  # noqa: E501
            raise ValidationError(u"Email Address must be unique")
        return email

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'language',)
