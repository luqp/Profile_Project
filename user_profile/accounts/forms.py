import re

from django import forms
from django.core import validators
from django.utils.html import escape
from django.contrib.auth import password_validation
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField, PasswordChangeForm)

from .models import User


def validate_not_containe(container, list_value):
    for value in list_value:
        if value.lower() in container.lower():
            raise forms.ValidationError(
                "Passwords don't have to contain the user's name")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'avatar',
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'bio'
        ]

    date_of_birth = forms.DateTimeField(
        widget=forms.DateInput(format='%m/%d/%Y'),
        input_formats=('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',)
    )
    bio = forms.CharField(widget=forms.Textarea,
                          validators=[validators.MinLengthValidator(10)])

    def clean_bio(self):
        bio = self.cleaned_data.get("bio")
        return escape(bio)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'date_of_birth')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        password_validation.validate_password(password2)
        return password2

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password2(self):
        old_password = self.cleaned_data.get("old_password")
        new_password2 = self.cleaned_data.get("new_password2")
        if old_password == new_password2:
            raise forms.ValidationError(
                "New passwords must be diferent than current password"
            )
        PasswordChangeForm.clean_new_password2(self)
        return new_password2
