from django.urls import path
from . import views

app_name = 'pybo' #네임스페이스 설정

urlpatterns = [
    #메인 pybo 페이지
    path('', views.index, name='index'), #-> pybo 이하에 urls.py이므로 이미 기본 url은 .../pybo/ 이다.

    #질문 상세 페이지 (상세, 댓글)
    path('<int:question_id>/', views.detail, name='detail'), #-> int:question_id -> question_id가 detail의 파라미터로 전달됨
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'), #답변등록

    #질문 등록
    path('question/create/', views.question_create, name='question_create'),
]