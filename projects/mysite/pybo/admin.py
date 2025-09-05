from django.contrib import admin
from .models import Question, Answer

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject'] #검색하는 필드(검색창느낌) -> subject(제목)을 입력하면 찾아주는듯
    #- https://docs.djangoproject.com/en/5.1/ref/contrib/admin/ 참고

# admin.site.register(Question)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)