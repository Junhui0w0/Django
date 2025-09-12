from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseNotAllowed
from django.utils import timezone
from ..models import Question, Answer, Pre_Question, Find_Question
from ..forms import QuestionForm, AnswerForm

from openpyxl import Workbook
import datetime
from urllib.parse import quote

from django.core.paginator import Paginator #- 한 페이지에 여러 개의 결과를 보여주는 것 방지
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse

from django.db.models import Q

def mainpage(request):
    return render(request, 'common/mainpage.html')

def board(request, category):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

    if category == 'pre':
        question_list = Pre_Question.objects.order_by('-create_date')
        if kw:
            question_list = question_list.filter(
                Q(subject__icontains=kw) |
                Q(send_name__icontains=kw) |
                Q(send_phone__icontains=kw) |
                Q(rec_name__icontains=kw) |
                Q(rec_phone__icontains=kw) |
                Q(product_type__icontains=kw)
            ).distinct()
    elif category == 'find':
        question_list = Find_Question.objects.order_by('-create_date')
        if kw:
            question_list = question_list.filter(
                Q(subject__icontains=kw) |
                Q(send_name__icontains=kw) |
                Q(send_phone__icontains=kw) |
                Q(rec_name__icontains=kw) |
                Q(rec_phone__icontains=kw) |
                Q(product_type__icontains=kw)
            ).distinct()
    else:
        question_list = Question.objects.filter(category=category).order_by('-create_date')
        if kw:
            question_list = question_list.filter(
                Q(subject__icontains=kw) |
                Q(content__icontains=kw)
            ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'category': category, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list.html', context)

# def index(request): #게시글 리스트 -> 한 페이지당 최대 10개의 게시글 출력하도록 할 것
#     # question_lst  = Question.objects.order_by('-create_date') # -create_date = 역방향 / create_date=정방향
#     # context = {'question_list':question_lst}
#     # return render(request, 'pybo/question_list.html', context)

#     page = request.GET.get('page', '1') #page 값을 가져온다. 이때, 기본값은 1
#     kw = request.GET.get('kw', '')  # 검색어
#     question_list = Question.objects.order_by('-create_date') #전체 게시글을 create_date 역순을 기준으로 불러옴
#     if kw:
#         question_list = question_list.filter(
#             Q(subject__icontains=kw) |  # 제목 검색
#             Q(content__icontains=kw)   # 내용 검색
#         ).distinct()

#     paginator = Paginator(question_list, 10) #불러온 게시글을 10개씩 나눔
#     page_obj = paginator.get_page(page) #page번호에 해당하는 게시글들 불러옴
#     context = {'question_list': page_obj, 'page': page, 'kw': kw} #해당 page에 있는 게시글들 정보를 context에 저장

#     return render(request, 'pybo/question_list.html', context)

@login_required(login_url='common:login')
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

    if not(request.user == question.author or request.user.is_superuser) and category in ('pre', 'find'): #요청한 사람이 작성자 또는 슈퍼유저가 아닌 경우 -> 권한없지
        return HttpResponseForbidden("해당 글은 작성자만 접근할 수 있습니다.")
        
    context = {'question': question, 'category': category}
    return render(request, template, context)

def extract_excel(request, category):
    # 1. 관리자(superuser) 권한 확인
    if not request.user.is_superuser:
        return HttpResponse("접근 권한이 없습니다.", status=403)
        
    # 2. GET 요청에서 선택된 게시글 ID 가져오기
    ids_string = request.GET.get('ids')
    if not ids_string:
        return HttpResponse("추출할 게시글을 선택해주세요.", status=400)
    
    selected_ids = ids_string.split(',')
    
    # 3. 데이터베이스에서 해당 게시글 데이터 가져오기
    if category == 'pre':
        questions = Pre_Question.objects.filter(id__in=selected_ids)
    elif category == 'find':
        questions = Find_Question.objects.filter(id__in=selected_ids)
    else:
        print(f'base_views #error - extract_excel - category 분류 실패')
        return HttpResponse("유효하지 않은 카테고리입니다.", status=400) # Better to return a proper HttpResponse

    # 4. Excel 파일 생성 및 데이터 작성
    wb = Workbook()
    ws = wb.active

    # 카테고리에 따라 시트 제목 및 헤더 설정
    if category == 'pre':
        ws.title = "택배사전접수"
        headers = ['보내는 분 성함', '보내는 분 연락처', '보내는 분 우편번호', '보내는 분 도로명 주소', '보내는 분 상세 주소',
                   '받는 분 성함', '받는 분 연락처', '받는 분 우편번호', '받는 분 도로명 주소', '받는 분 상세 주소',
                   '상품 종류', '수량', '지불 방식', '포장 형식']
    elif category == 'find':
        ws.title = "택배찾기"
        headers = ['보내는 분 성함', '보내는 분 연락처', '보내는 분 우편번호', '보내는 분 도로명 주소', '보내는 분 상세 주소',
                   '상품 종류', '포장 형식', '수량']
    else:
        return HttpResponse("유효하지 않은 카테고리입니다.", status=400)

    ws.append(headers)

    # 데이터 추출 및 행에 추가
    rows = []
    if category == 'pre':
        for q in questions:
            row = [
                q.send_name, q.send_phone, q.send_addr_zipcode, q.send_addr_road, q.send_addr_detail,
                q.rec_name, q.rec_phone, q.rec_addr_zipcode, q.rec_addr_road, q.rec_addr_detail,
                q.product_type, q.num
            ]

            # 포장 형식 변환 및 추가
            str_package_type = q.package_type if q.package_type else '정보 없음'
            if str_package_type == 'vinyl': str_package_type = '비닐'
            elif str_package_type == 'naked': str_package_type = '나체'
            elif str_package_type == 'box': str_package_type = '박스'
            elif str_package_type == 'custom': str_package_type = '포장-custom'
            row.append(str_package_type)

            # 지불 방식 변환 및 추가
            str_pay_method = q.pay_method if hasattr(q, 'pay_method') and q.pay_method else '정보 없음'
            if str_pay_method == 'at_now': str_pay_method = '현불'
            elif str_pay_method == 'at_delivered': str_pay_method = '착불'
            row.append(str_pay_method)
            
            rows.append(row)

    elif category == 'find':
        for q in questions:
            row = [
                q.send_name, q.send_phone, q.send_addr_zipcode, q.send_addr_road, q.send_addr_detail,
                q.product_type, q.num
            ]
            
            # 포장 형식 변환 및 추가
            str_package_type = q.package_type if hasattr(q, 'package_type') and q.package_type else '정보 없음'
            if str_package_type == 'vinyl': str_package_type = '비닐'
            elif str_package_type == 'naked': str_package_type = '나체'
            elif str_package_type == 'box': str_package_type = '박스'
            elif str_package_type == 'custom': str_package_type = '포장-custom'
            row.append(str_package_type)
            
            rows.append(row)
            
    for row_data in rows:
        ws.append(row_data)

    # 5. Excel 컬럼 너비 자동 조정 (Fix #2)
    idx = 0
    for col in ws.columns:
        print(f'{idx}번쨰 col 데이터: {col}')
        idx += 1

        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
                    print(f'idx: {idx} // max_len: {max_length} // string:{cell.value}')
            except:
                pass

        if max_length <= 4:
            max_length = 6

        adjusted_width = (max_length * 1.7)
        ws.column_dimensions[column].width = adjusted_width

    # 6. HTTP 응답 생성 및 파일 다운로드 (Fix #1)
    now = datetime.datetime.now().strftime('%Y%m%d')
    file_name = f"{now}_{ws.title}.xlsx"
    
    # URL 인코딩을 적용하여 파일명에 한글이 포함되어도 깨지지 않게 함
    encoded_file_name = quote(file_name) 

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f"attachment; filename*=UTF-8''{encoded_file_name}"
    
    # 워크북을 HTTP 응답으로 저장하고 반환
    wb.save(response)
    return response