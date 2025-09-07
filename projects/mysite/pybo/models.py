from django.db import models
from django.contrib.auth.models import User

# Create your models here. -> DB에 저장될 흠.. 테이블? 느낌인듯 col 정의하는 곳
# https://docs.djangoproject.com/en/5.1/ref/models/fields/#field-types -> 데이터 타입 
class Question(models.Model):
    subject = models.CharField(max_length=200)
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