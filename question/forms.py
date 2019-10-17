from django import forms
from .models import QuestionModel, AnswerModel, QuestionReportModel


class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        fields = [
            'questionTitle',
            'questionContent',
            'categoryID',
            'emailNotifications',
        ]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = AnswerModel
        fields = [
            'answer',
        ]


class QuestionReport(forms.ModelForm):
    class Meta:
        model = QuestionReportModel
        fields = [
            'reportReason',
        ]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = AnswerModel
        fields = [
            'answer',
        ]


class EditAnswerForm(forms.ModelForm):
    class Meta:
        model = AnswerModel
        fields = [
            'answer',
        ]
