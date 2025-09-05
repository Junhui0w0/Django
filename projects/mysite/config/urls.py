"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include #- 앱 전용 url은 include로 처리
from .views import mainpage

# from pybo import views

#첫 사이트 메인 url
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('pybo/', views.index),
    #path(url경로, 호출할 뷰 함수)
    path('pybo/', include('pybo.urls')), #-> .../pybo/ETC & .../pybo/ETC2 등 pybo로 시작하는 url을 추가할 때 pybo.urls만 수정하면 됨
    path('', mainpage)
]
