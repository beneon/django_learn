from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('age','desc')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = UserChangeForm.Meta.fields
