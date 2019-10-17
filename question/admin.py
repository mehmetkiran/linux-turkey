from django.contrib import admin
from .models import *


@admin.register(QuestionModel)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['questionTitle', 'questionCreateDate', 'questionEditDate', 'slug']
    list_display_links = ['questionTitle', 'questionCreateDate', 'questionEditDate', ]


@admin.register(QuestionCategoryModel)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ['categoryName', ]
    list_display_links = ['categoryName', ]


@admin.register(AnswerModel)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['userID', 'answer', 'answerDate', 'bestAnswer', ]
    list_display_links = ['userID', 'answer', 'answerDate', 'bestAnswer', ]


@admin.register(QuestionReportModel)
class QuestionReportModelAdmin(admin.ModelAdmin):
    list_display = ['reportID']


@admin.register(ScoreModel)
class ScoreModelAdmin(admin.ModelAdmin):
    list_display = ['score_status', 'user', 'answer']
    list_display_links = ['score_status', 'user', 'answer']
