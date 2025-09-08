from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseNotAllowed
from django.utils import timezone
from ..models import Question, Answer, Pre_Question, Find_Question
from ..forms import QuestionForm, AnswerForm, Pre_QuestionForm, Find_QuestionForm

from django.core.paginator import Paginator #- 한 페이지에 여러 개의 결과를 보여주는 것 방지
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#카테고리별 글 작성
@login_required(login_url='common:login')
def category_question_create(request, category): #질문등록
    #카테고리=pre -> Pre_QuestionForm 사용
    if category == 'pre':

        today = timezone.now().strftime('%Y-%m-%d')
        username = request.user.username if request.user.is_authenticated else ''

        form = Pre_QuestionForm()
        
        if request.method == 'POST':
            form = Pre_QuestionForm(request.POST)

            if form.is_valid():
                question = form.save(commit=False)
                question.subject = f'택배 사전 접수 | {today} | {username}'
                question.create_date = timezone.now()
                question.category = category
                question.author = request.user

                if request.POST.get('package_type') == 'custom':
                    custom_package_type = request.POST.get('custom_package_type')
                    print(custom_package_type)
                    question.package_type = custom_package_type

                if request.POST.get('num') == 'custom':
                    custom_num = request.POST.get('custom_num')
                    # print(custom_num)
                    question.num = custom_num

                question.save()
                return redirect('pybo:board', category=category)
            
        else:
            initial_subject = f'택배 사전 접수 | {today} | {username}'

            form = Pre_QuestionForm(initial={'subject': initial_subject})

        context = {'form': form, 'category': category}
        return render(request, 'pybo/pre_question_form.html', context)

    #카테고리=find -> Find_QuestionForm 사용
    elif category == 'find':

        today = timezone.now().strftime('%Y-%m-%d')
        username = request.user.username if request.user.is_authenticated else ''

        form = Find_QuestionForm()
        
        if request.method == 'POST':
            form = Find_QuestionForm(request.POST)

            if form.is_valid():
                question = form.save(commit=False)
                question.create_date = timezone.now()
                question.subject = f'택배 찾기 | {today} | {username}'
                question.category = category
                question.author = request.user

                if request.POST.get('package_type') == 'custom':
                    custom_package_type = request.POST.get('custom_package_type')
                    # print(custom_package_type)
                    question.package_type = custom_package_type

                if request.POST.get('num') == 'custom':
                    custom_num = request.POST.get('custom_num')
                    # print(custom_num)
                    question.num = custom_num


                question.save()
                return redirect('pybo:board', category=category)
            
        else:
            initial_subject = f'택배 찾기 | {today} | {username}'

            form = Find_QuestionForm(initial={'subject': initial_subject})

        context = {'form': form, 'category': category}
        return render(request, 'pybo/find_question_form.html', context)





    #카테고리=notice or qna -> QuestionForm 사용
    elif category in ['notice', 'qna']:
        if category == 'notice':
            category_name = '공지사항'
        elif category == 'qna':
            category_name = '문의하기'

        today = timezone.now().strftime('%Y-%m-%d')
        username = request.user.username if request.user.is_authenticated else ''

        form = QuestionForm()
        
        if request.method == 'POST':
            form = QuestionForm(request.POST)

            if form.is_valid(): #유효성 검사
                question = form.save(commit=False) #commit=False -> 임시저장
                # question.subject = f'{category_name} | {today} | {username}'
                question.create_date = timezone.now()
                question.category = category
                question.author = request.user
                question.save()
                return redirect('pybo:board', category=category)
            
            
        else:
            # initial_subject = f'{category_name} | {today} | {username}'

            form = QuestionForm()

        context = {'form': form, 'category': category}
        return render(request, 'pybo/question_form.html', context)




#카테고리별 글 삭제
@login_required(login_url='common:login')
def category_question_delete(request, category, question_id):

    if category == 'pre':
        question = get_object_or_404(Pre_Question, pk=question_id)

    elif category == 'find':
        question = get_object_or_404(Find_Question, pk=question_id)

    elif category in ('qna', 'notice'): 
        question = get_object_or_404(Question, pk=question_id)

    if request.user == question.author or request.user.is_superuser:
        question.delete()
        return redirect('pybo:board', category=category)
    
    messages.error(request, '삭제권한이 없습니다')
    context = {question_id: question_id, category: category}
    return redirect('pybo:detail', context)


@login_required(login_url='common:login')
def category_question_processed(request, category, question_id):
    if category == 'pre':
        question = get_object_or_404(Pre_Question, pk=question_id)

    elif category == 'find':
        question = get_object_or_404(Find_Question, pk=question_id)

    elif category in ('qna', 'notice'):
        question = get_object_or_404(Question, pk=question_id)

    if request.user.is_superuser:
        question.processed = True #처리완료
        print(question.processed)
        question.save()

    print(f'현재 제목: {question.subject}')
    return redirect('pybo:board', category=category)

#카테고리별 글 수정
@login_required(login_url='common:login') #흠.. 애초에 로그인 한 사람 정보를 기반으로 보이게 할 텐데 필요한가?
def category_question_modify(request, category, question_id):

    if category == 'pre':
        return True
    
    elif category == 'find':
        return True
    
    elif category in ('qna', 'notice'):
        question = get_object_or_404(Question, pk=question_id)

        if request.user == question.author:
            if request.method == "POST": #수정하기 버튼을 눌러 팝업된 html form을 채워서 submit 버튼을 눌렀을 때 -> POST
                form = QuestionForm(request.POST, instance=question)
                if form.is_valid():
                    question = form.save(commit=False)
                    question.modify_date = timezone.now()
                    question.category = category
                    question.save()
                    return redirect('pybo:detail', question_id=question.id, category=category)
            else:
                form = QuestionForm(instance=question) #수정하기 버튼을 누른 경우 -> Html form 요청(GET)

            context = {'form': form, 'category': category}
            return render(request, 'pybo/question_form.html', context) #-> pybo의 question_form.html로 이동
    



#카테고리별 글 추천
@login_required(login_url='common:login')
def category_question_vote(request, question_id, category):
    question = get_object_or_404(Question, pk=question_id)

    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        question.voter.add(request.user)

    return redirect('pybo:detail', question_id=question.id, category=category)






#===============================================

# @login_required(login_url='common:login')
# def question_create(request): #질문등록
#     form = QuestionForm()
    
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)

#         if form.is_valid(): #유효성 검사
#             question = form.save(commit=False) #commit=False -> 임시저장
#             question.create_date = timezone.now()
#             question.author = request.user
#             question.save()
#             return redirect('pybo:index')
        
#     else:
#         form = QuestionForm()

#     return render(request, 'pybo/question_form.html', {'form':form})


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