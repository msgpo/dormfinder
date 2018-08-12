# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SohaeUser

class SohaeUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = SohaeUser
        fields = ('username', 'email')


class SohaeUserChangeForm(UserChangeForm):
    class Meta:
        model = SohaeUser
        fields = UserChangeForm.Meta.fields