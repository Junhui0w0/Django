from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
        #기본적으로 auth_views.LoginView를 사용하면 registration 템플릿을 찾지만,
        #template_name 속성을 사용해 경로를 지정할 수 있음.
        
        #django.contrib.auth 패키지는 로그인이 성공하면 /accounts/profile로 이동함
        #이를 변경하기 위해선 settings.py -> LOGIN_REDIRECT_URL 속성을 설정해야 함.

        path('logout/', views.logout_view, name='logout'),
        path('signup/', views.signup, name='signup'),
]

