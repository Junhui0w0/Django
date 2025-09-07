from django.shortcuts import render, get_object_or_404, redirect, resolve_url
# from django.http import HttpResponseNotAllowed
from django.utils import timezone
from ..models import Question, Answer
from ..forms import QuestionForm, AnswerForm

from django.core.paginator import Paginator #- 한 페이지에 여러 개의 결과를 보여주는 것 방지
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user == answer.author:
        if request.method == "POST": #-> GET에서 받아온 HTML 폼 정보를 채운 후 submit 버튼을 눌렀을 때
            form = AnswerForm(request.POST, instance=answer) #기존 answer 정보를 instance로
            if form.is_valid():
                answer = form.save(commit=False)
                answer.modify_date = timezone.now()
                answer.save()
                return redirect('{}#answer_{}'.format(
                    resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
            
        else: #-> GET인 경우 -> 수정하는 HTML 폼 요청
            form = AnswerForm(instance=answer)

        context = {'answer': answer, 'form': form}
        return render(request, 'pybo/answer_form.html', context)
    
    #수정 권한 없는 경우
    messages.error(request, '수정권한이 없습니다')
    return redirect('pybo:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user == answer.author or request.user.is_superuser:
        answer.delete()
        return redirect('pybo:detail', question_id=answer.question.id)
    
    messages.error(request, '삭제권한이 없습니다')
    return redirect('pybo:detail', question_id=answer.question.id)

#댓글 추천
@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        answer.voter.add(request.user)

    return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))