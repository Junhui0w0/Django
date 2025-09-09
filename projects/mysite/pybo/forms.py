from django import forms
from pybo.models import Question, Answer, Pre_Question, Find_Question

PACKAGE_CHOICES = [
    ('naked', '나체'),
    ('box', '박스'),
    ('vinyl', '비닐'),
    ('madae', '마대'),
    ('custom', '직접 입력'),  # 추가!
]

NUM_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('custom', '직접 입력'),
]

PAY_METHOD = [
    ('at_now', '현불'),
    ('at_delivered', '착불'),
]

class Pre_QuestionForm(forms.ModelForm):
    package_type = forms.ChoiceField(choices=PACKAGE_CHOICES, label='포장 형식')
    num = forms.ChoiceField(choices=NUM_CHOICES, label='수량')  # 1부터 10까지의 수량 선택지
    pay_method = forms.ChoiceField(choices=PAY_METHOD, label='지불 방식')

    class Meta: #ModelForm에서는 필수
        model = Pre_Question #사용 할 모델
        fields = ['subject', 'send_name', 'send_phone', 'send_addr_zipcode', 'send_addr_road', 'send_addr_detail', 'rec_name', 'rec_phone', 'rec_addr_zipcode', 'rec_addr_road', 'rec_addr_detail', 'product_type', 'package_type', 'num', 'pay_method'] #QuestionForm에서 사용할 Queston 모델의 속성들
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        # }
        labels = {
            'subject': '제목',
            'send_name': '보내는 분 성함',
            'send_phone': '보내는 분 연락처',
            'send_addr_zipcode': '보내는 분 우편주소',
            'send_addr_road': '보내는 분 도로명 주소',
            'send_addr_detail': '보내는 분 상세 주소',

            'rec_name': '받는 분 성함',
            'rec_phone': '받는 분 연락처',
            'rec_addr_zipcode': '받는 분 우편주소',
            'rec_addr_road': '받는 분 도로명 주소',
            'rec_addr_detail': '받는 분 상세 주소',
            'product_type': '상품 종류',
            'package_type': '포장 형식',
            'num': '수량',
            'pay_method': '지불 방식',
        }  

class Find_QuestionForm(forms.ModelForm):
    package_type = forms.ChoiceField(choices=PACKAGE_CHOICES, label='포장 형식')
    num = forms.ChoiceField(choices=NUM_CHOICES, label='수량') 

    class Meta: #ModelForm에서는 필수
        model = Find_Question #사용 할 모델
        fields = ['subject', 'send_name', 'send_phone', 'send_addr_zipcode', 'send_addr_road', 'send_addr_detail', 'product_type', 'package_type', 'num'] #QuestionForm에서 사용할 Queston 모델의 속성들

        labels = {
            'subject': '제목',
            'send_name': '보내는 분 성함',
            'send_phone': '보내는 분 연락처',
            'send_addr_zipcode': '보내는 분 우편주소',
            'send_addr_road': '보내는 분 도로명 주소',
            'send_addr_detail': '보내는 분 상세 주소',
            
            'product_type': '상품 종류',
            'package_type': '포장 형식',
            'num': '수량',
        } 


class QuestionForm(forms.ModelForm):
    class Meta: #ModelForm에서는 필수
        model = Question #사용 할 모델
        fields = ['subject', 'content'] #QuestionForm에서 사용할 Queston 모델의 속성들
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        # }
        labels = {
            'subject': '제목',
            'content': '내용',
        }  

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }