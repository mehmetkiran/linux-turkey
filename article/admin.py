from django.contrib import admin

from .models import ArticleModel, CommentModel


@admin.register(ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['articleTitle', 'articleContent', 'articleViewCounter', 'articleCreateDate', 'articleAuthor',
                    'slug', ]
    list_filter = ['articleCreateDate', ]


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'commentDate']
