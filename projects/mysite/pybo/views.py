from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


def index(request): #게시글 리스트
    question_lst  = Question.objects.order_by('-create_date') # -create_date = 역방향 / create_date=정방향
    context = {'question_list':question_lst}
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

def question_create(request): #질문등록
    form = QuestionForm()
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid(): #유효성 검사
            question = form.save(commit=False) #commit=False -> 임시저장
            question.create_date = timezone.now()
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
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)