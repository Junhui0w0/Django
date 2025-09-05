from django.db import models

# Create your models here. -> DB에 저장될 흠.. 테이블? 느낌인듯 col 정의하는 곳
# https://docs.djangoproject.com/en/5.1/ref/models/fields/#field-types -> 데이터 타입 
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #앞의 모델(Question)이 사라지면 댓글도 자동 삭제
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        title = f'[댓글] {self.question.subject}'
        return title

