from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseNotAllowed
from django.utils import timezone
from ..models import Question, Answer
from ..forms import QuestionForm, AnswerForm

from django.core.paginator import Paginator #- 한 페이지에 여러 개의 결과를 보여주는 것 방지
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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


@login_required(login_url='common:login') #흠.. 애초에 로그인 한 사람 정보를 기반으로 보이게 할 텐데 필요한가?
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user == question.author:
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


    messages.error(request, '수정권한이 없습니다')
    return redirect('pybo:detail', question_id=question.id) #pybo의 urls.py에서 name=detail인 url로 이동


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user == question.author or request.user.is_superuser:
        question.delete()
        return redirect('pybo:index')
    
    messages.error(request, '삭제권한이 없습니다')
    return redirect('pybo:detail', question_id=question.id)
    
@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        question.voter.add(request.user)

    return redirect('pybo:detail', question_id=question.id)