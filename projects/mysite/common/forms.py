from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm): #UserForm을 UserCreationForm을 상속받아 만듦

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
            #username, password1, password2는 UserCreationForm에 이미 정의되어 있음.