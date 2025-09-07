from django.urls import path
from .views import base_views, question_views, answer_views

app_name = 'pybo' #네임스페이스 설정

urlpatterns = [
    #메인 pybo 페이지
    path('', base_views.index, name='index'), #-> pybo 이하에 urls.py이므로 이미 기본 url은 .../pybo/ 이다.

    #질문 상세 페이지 (상세, 댓글)
    path('<int:question_id>/', base_views.detail, name='detail'), #-> int:question_id -> question_id가 detail의 파라미터로 전달됨
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'), #답변등록

    #질문 등록
    path('question/create/', question_views.question_create, name='question_create'),
    
    #수정 등록
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),

    #삭제
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),

    #답변 수정
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),

    #답변 삭제
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),

    #추천 - 게시글
    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),

    #추천 - 댓글
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'),
]