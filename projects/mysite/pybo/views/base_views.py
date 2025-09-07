from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseNotAllowed
from django.utils import timezone
from ..models import Question, Answer, Pre_Question, Find_Question
from ..forms import QuestionForm, AnswerForm

from django.core.paginator import Paginator #- 한 페이지에 여러 개의 결과를 보여주는 것 방지
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Q

def mainpage(request):
    return render(request, 'common/mainpage.html')

def board(request, category):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

    if category == 'pre':
        question_list = Pre_Question.objects.order_by('-create_date')
    elif category == 'find':
        question_list = Find_Question.objects.order_by('-create_date')
    else:
        question_list = Question.objects.filter(category=category).order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            # Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
            # Q(create_date__date=kw)
        ).distinct()
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'category': category, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list.html', context)

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


def detail(request, category, question_id): #게시글 상세
    if category == 'pre':
        question = get_object_or_404(Pre_Question, pk=question_id)
        template = 'pybo/pre_question_detail.html'
    elif category == 'find':
        question = get_object_or_404(Find_Question, pk=question_id)
        template = 'pybo/find_question_detail.html'
    else:
        question = get_object_or_404(Question, pk=question_id)
        template = 'pybo/question_detail.html'
        
    context = {'question': question, 'category': category}
    return render(request, template, context)
