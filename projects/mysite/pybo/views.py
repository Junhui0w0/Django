from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseNotAllowed
from django.utils import timezone
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

from django.core.paginator import Paginator #- 한 페이지에 여러 개의 결과를 보여주는 것 방지
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request): #게시글 리스트 -> 한 페이지당 최대 10개의 게시글 출력하도록 할 것
    # question_lst  = Question.objects.order_by('-create_date') # -create_date = 역방향 / create_date=정방향
    # context = {'question_list':question_lst}
    # return render(request, 'pybo/question_list.html', context)

    page = request.GET.get('page', '1') #page 값을 가져온다. 이때, 기본값은 1
    question_list = Question.objects.order_by('-create_date') #전체 게시글을 create_date 역순을 기준으로 불러옴

    paginator = Paginator(question_list, 10) #불러온 게시글을 10개씩 나눔
    page_obj = paginator.get_page(page) #page번호에 해당하는 게시글들 불러옴
    context = {'question_list': page_obj} #해당 page에 있는 게시글들 정보를 context에 저장

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id): #게시글 상세
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id) #pk=primary key -> 데이터가 없어서 505 에러가 발생해도 404 출력
    context={'question':question}

    return render(request, 'pybo/question_detail.html', context)

# def answer_create(request, question_id): #답변등록
#     question = get_object_or_404(Question, pk=question_id) #505 에러 -> 404 에러 처리
#     question.answer_set.create(content=request.POST.get('content'), create_date='2024-06-11 12:00') #answer_set -> ForeignKey로 연결된 answer테이블에 접근
    
#     #모델2 = answer / 모델1=question -> answer의 외래키 = question -> question.answer_set
    
#     #혹은 아래와 같이 사용 가능
#     #answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    
#     return redirect('pybo:detail', question_id=question.id) #답변등록 후 질문 상세화면으로 이동

@login_required(login_url='common:login')
def question_create(request): #질문등록
    form = QuestionForm()
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid(): #유효성 검사
            question = form.save(commit=False) #commit=False -> 임시저장
            question.create_date = timezone.now()
            question.author = request.user
            question.save()
            return redirect('pybo:index')
        
    else:
        form = QuestionForm()

    return render(request, 'pybo/question_form.html', {'form':form})

def answer_create(request, question_id): #답변등록
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user

            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login') #흠.. 애초에 로그인 한 사람 정보를 기반으로 보이게 할 텐데 필요한가?
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id) #pybo의 urls.py에서 name=detail인 url로 이동
    
    if request.method == "POST": #수정하기 버튼을 눌러 팝업된 html form을 채워서 submit 버튼을 눌렀을 때 -> POST
        form = QuestionForm(request.POST, instance=question) #일차적으로 기존 question 정보를 씀 -> 이후에 request.post 정보를 덮어씀
        if form.is_valid():
            question = form.save(commit=False) #일시저장
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question) #수정하기 버튼을 누른 경우 -> Html form 요청(GET)

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context) #-> pybo의 question_form.html로 이동


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    
    question.delete()
    return redirect('pybo:index')