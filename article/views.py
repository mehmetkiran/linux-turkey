import os
import sweetify
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from article.models import ArticleModel, CommentModel
from .forms import ArticleForm_, CommentForm_

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_TEMPLATE = os.path.join(BASE_DIR, 'templates/components/')
COMPONENTS = os.path.join(BASE_DIR, 'templates/components/commonComponents/')


def blog_home_view(request):
    if request.user.is_authenticated:
        base_template = os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html')
        login_panel = os.path.join(COMPONENTS, 'widget_login_session.html')
    else:
        base_template = os.path.join(BASE_TEMPLATE, 'nonSessionComponents/navbar.html')
        login_panel = os.path.join(COMPONENTS, 'widget_login.html')

    article_ = ArticleModel.objects.order_by('-articleCreateDate')
    article_slider = article_[:2]

    article_paginator = Paginator(article_, 20)
    page = request.GET.get('page')

    try:
        article = article_paginator.get_page(page)
    except PageNotAnInteger:
        article = article_paginator.page(1)
    except EmptyPage:
        article = article_paginator.page(article_paginator.num_pages)

    context = {'base_template': base_template,
               'article_': article, 'article_slider': article_slider,
               'loginPanel': login_panel}
    return render(request, 'apps/article/index.html', context)


def read_article_view(request, article_id):
    article = get_object_or_404(ArticleModel, id=article_id)
    answer = CommentModel.objects.filter(articleID=article_id)
    random_question = ArticleModel.objects.order_by('?')[:4]

    answer_count = answer.count()

    if request.user.is_authenticated:
        comment_form = CommentForm_(request.POST or None)
        if comment_form.is_valid():
            form = comment_form.save(commit=False)
            form.userID = request.user
            form.articleID_id = article_id
            form.save()
            sweetify.success(request, 'Cevap oluşturuldu şimdi yönlediriliyorsunuz')

        context = {'base_template': os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html'),
                   'article': article, 'answer': answer, 'answercount': answer_count,
                   'commentForm': comment_form, 'random_question': random_question,
                   'loginPanel': os.path.join(COMPONENTS, 'widget_login_session.html')}

        return render(request, 'apps/article/readArticle.html', context)
    else:
        context = {'base_template': os.path.join(BASE_TEMPLATE, 'nonSessionComponents/navbar.html'), 'article': article,
                   'answer': answer, 'answercount': answer_count,
                   'random_question': random_question,
                   'loginPanel': os.path.join(COMPONENTS, 'widget_login.html')}
        return render(request, 'apps/article/readArticle.html', context)


def show_category_view(request, category_id):
    category_id_ = ArticleModel.objects.filter(categoryName=category_id).order_by('-articleCreateDate')
    if request.user.is_authenticated:
        context = {'base_template': os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html'),
                   'categoryID_': category_id_,
                   'loginPanel': os.path.join(COMPONENTS, 'widget_login_session.html')}
        return render(request, 'apps/article/articleCategory.html', context)
    else:
        context = {'base_template': os.path.join(BASE_TEMPLATE, 'nonSessionComponents/navbar.html'),
                   'categoryID_': category_id_,
                   'loginPanel': os.path.join(COMPONENTS, 'widget_login.html')}
        return render(request, 'apps/article/articleCategory.html', context)


@permission_required('article.create_article_view')
def create_article_view(request):
    if request.user.is_authenticated:
        article_form = ArticleForm_(request.POST or None, request.FILES or None)
        if article_form.is_valid():
            form = article_form.save(commit=False)
            form.articleAuthor = request.user
            form.save()
            sweetify.success(request, 'Makale oluşturuldu şimdi yönlediriliyorsunuz', timer=2000)
            return redirect('home:home')

        context = {'base_template': os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html'),
                   'loginPanel': os.path.join(COMPONENTS, 'widget_login_session.html'), 'articleForm': article_form}
        return render(request, 'apps/article/addArticle.html', context)
    else:
        return redirect('user:login')


def create_pdf_view(request):
    pass
