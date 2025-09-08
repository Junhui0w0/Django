from django.db import models
from django.contrib.auth.models import User

# Create your models here. -> DB에 저장될 흠.. 테이블? 느낌인듯 col 정의하는 곳
# https://docs.djangoproject.com/en/5.1/ref/models/fields/#field-types -> 데이터 타입 
class Pre_Question(models.Model): #택배 사전 접수
    CATEGORY_CHOICES = [
        ('pre', '택배 사전 접수'),
        ('find', '택배 찾기'),
        ('qna', '문의하기'),
        ('notice', '공지사항'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='pre')

    processed = models.BooleanField(default=False)

    subject = models.CharField(max_length=500, blank=True)
    send_name = models.CharField(max_length=50) #보내는 분 성함
    send_phone = models.CharField(max_length=20) #보내는 분 연락처

    send_addr = models.CharField(max_length=200, blank=True, null=True) #보내는 분 주소

    rec_name = models.CharField(max_length=50) #받는 분 성함
    rec_phone = models.CharField(max_length=20) #받는 분 연락처

    rec_addr = models.CharField(max_length=200, blank=True, null=True) #받는 분 주소

    product_type = models.CharField(max_length=100) #상품 종류
    package_type = models.CharField(max_length=20) #포장 형식
    num = models.CharField(max_length=10) #수량

    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_pre_question') #User가 삭제되면 질문도 삭제
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_pre_question') 

    def __str__(self):
        return self.subject

class Find_Question(models.Model):
    processed = models.BooleanField(default=False)

    subject = models.CharField(max_length=200, blank=True)
    send_name = models.CharField(max_length=50) #보내는 분 성함
    send_phone = models.CharField(max_length=20) #보내는 분 연락처

    send_addr = models.CharField(max_length=200, blank=True, null=True) #보내는 분 주소

    product_type = models.CharField(max_length=100) #상품 종류
    package_type = models.CharField(max_length=20) #포장 형식
    num = models.CharField(max_length=10) #수량

    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_find_question') #User가 삭제되면 질문도 삭제
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_find_question') 

    def __str__(self):
        return self.subject

class Question(models.Model): #공지 / 질문
    processed = models.BooleanField(default=False)
    
    CATEGORY_CHOICES = [
        ('qna', '문의하기'),
        ('notice', '공지사항'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='qna')

    subject = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_question') #User가 삭제되면 질문도 삭제
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question') 

    def __str__(self):
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #앞의 모델(Question)이 사라지면 댓글도 자동 삭제
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_answer') #User가 삭제되면 답변도 삭제
    modify_date = models.DateTimeField(null=True, blank=True)
        #null=True -> DB에 null 허용
        #blank=True -> 추후 form.is_valid()에서 값에 상관없이 검증 통과
        #수정하는 경우는 데이터를 생성할 때가 아닌, 수정할 때만 생기므로 -> null값과 유효성 검사를 통과할 수 있다.
    voter = models.ManyToManyField(User, related_name='voter_answer') 

    def __str__(self):
        title = f'[댓글] {self.question.subject}'
        return title

# class Comment(models.Model):