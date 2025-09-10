from django.urls import path
from .views import base_views, question_views, answer_views

app_name = 'pybo' #네임스페이스 설정

urlpatterns = [
    #메인 pybo 페이지

    #질문 상세 페이지 (상세, 댓글)
    path('board/<str:category>/<int:question_id>/', base_views.detail, name='detail'),

    #===============================================

    #메인페이지 - 카테고리별 게시판
    path('board/<str:category>/', base_views.board, name='board'),

    #카테고리별 질문 작성
    path('board/<str:category>/create/', question_views.category_question_create, name='category_question_create'),

    #카테고리별 질문 삭제
    path('board/<str:category>/delete/<int:question_id>/', question_views.category_question_delete, name='category_question_delete'),

    #카테고리별 질문 수정
    path('board/<str:category>/modify/<int:question_id>/', question_views.category_question_modify, name='category_question_modify'),

    #카테고리별 게시글 처리완료
    path('board/<str:category>/processed/<int:question_id>/', question_views.category_question_processed, name='category_question_processed'),


    #===============================================

    #카테고리별 답변 등록
    path('answer/create/<int:question_id>/<str:category>/', answer_views.category_answer_create, name='category_answer_create'), #답변등록

    #카테고리별 답변 수정
    path('answer/modify/<int:answer_id>/', answer_views.category_answer_modify, name='category_answer_modify'),

    #카테고리별 답변 삭제
    path('answer/delete/<int:answer_id>/', answer_views.category_answer_delete, name='category_answer_delete'),

    #카테고리(pre/find) 정보 추출
    path('board/<str:category>/extract/', base_views.extract_excel, name='extract_excel'),

    #===============================================

    #카테고리별 게시글 추천
    path('question/vote/<int:question_id>/<str:category>/', question_views.category_question_vote, name='category_question_vote'),

    #카테고리별 댓글 추천
    path('answer/vote/<int:answer_id>/', answer_views.category_answer_vote, name='category_answer_vote'),
]
