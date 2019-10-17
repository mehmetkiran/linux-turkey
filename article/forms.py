from django import forms
from .models import *


class ArticleForm_(forms.ModelForm):
    class Meta:
        model = ArticleModel
        fields = [
            'articleTitle',
            'articleContent',
            'categoryName',
            'articleCoverImage',
        ]


class CommentForm_(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = [
            'comment',
        ]
