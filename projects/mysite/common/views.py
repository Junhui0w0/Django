from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from common.forms import UserForm
# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('mainpage')

def signup(request):
    if request.method == "POST": #데이터를 전송한다. = 회원가입 폼을 채워서 서버에 전송한다
        form = UserForm(request.POST) #폼 객체 생성
        
        if form.is_valid(): #폼이 유효하다면
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user) #회원가입 후 자동 로그인
            return redirect('mainpage')
        
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def page_not_found(request, exception):
    return render(request, 'common/404.html', {})