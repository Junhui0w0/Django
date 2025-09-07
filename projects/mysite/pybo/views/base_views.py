from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseNotAllowed
from django.utils import timezone
from ..models import Question, Answer
from ..forms import QuestionForm, AnswerForm

from django.core.paginator import Paginator #- 한 페이지에 여러 개의 결과를 보여주는 것 방지
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Q

def index(request): #게시글 리스트 -> 한 페이지당 최대 10개의 게시글 출력하도록 할 것
    # question_lst  = Question.objects.order_by('-create_date') # -create_date = 역방향 / create_date=정방향
    # context = {'question_list':question_lst}
    # return render(request, 'pybo/question_list.html', context)

    page = request.GET.get('page', '1') #page 값을 가져온다. 이때, 기본값은 1
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date') #전체 게시글을 create_date 역순을 기준으로 불러옴
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw) |  # 답변 글쓴이 검색
            # Q(modify_date__icontains=kw) | # 질문 날짜 검색
            Q(create_date__date=kw)   # 답변 날짜 검색
        ).distinct()

    paginator = Paginator(question_list, 10) #불러온 게시글을 10개씩 나눔
    page_obj = paginator.get_page(page) #page번호에 해당하는 게시글들 불러옴
    context = {'question_list': page_obj, 'page': page, 'kw': kw} #해당 page에 있는 게시글들 정보를 context에 저장

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id): #게시글 상세
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id) #pk=primary key -> 데이터가 없어서 505 에러가 발생해도 404 출력
    context={'question':question}

    return render(request, 'pybo/question_detail.html', context)