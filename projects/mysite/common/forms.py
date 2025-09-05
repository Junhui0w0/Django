from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm): #UserForm을 UserCreationForm을 상속받아 만듦
    email = forms.EmailField(label="이메일")
        #회원가입 폼에 추가시킬 새로운 속성(이메일)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")
            #username, password1, password2는 UserCreationForm에 이미 정의되어 있음.
            #email은 우리가 새로 추가한 속성.
