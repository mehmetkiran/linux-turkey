from django.shortcuts import render
from article.models import ArticleModel
from user.models import UserModel
from .forms import *
from question.models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import sweetify
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_TEMPLATE = os.path.join(BASE_DIR, 'templates/components/')
COMPONENTS = os.path.join(BASE_DIR, 'templates/components/commonComponents/')


def home_view(request):
    # Last Questions Start
    questions = QuestionModel.objects.order_by('-id')
    question_paginator = Paginator(questions, 20)
    page = request.GET.get('page')

    try:
        question_page = question_paginator.get_page(page)
    except PageNotAnInteger:
        question_page = question_paginator.page(1)
    except EmptyPage:
        question_page = question_paginator.page(question_paginator.num_pages)
    # Last Questions End

    # Not Answered Question Start
    answer_id = AnswerModel.objects.values_list('questionID', flat=True).distinct()
    not_answered = QuestionModel.objects.exclude(id__in=answer_id).order_by('-questionCreateDate')

    not_answered_paginator = Paginator(not_answered, 20)
    not_answered_page = request.GET.get('notAnsweredPage')

    try:
        not_answered_ = not_answered_paginator.get_page(not_answered_page)
    except PageNotAnInteger:
        not_answered_ = not_answered_paginator.page(1)
    except EmptyPage:
        not_answered_ = not_answered_paginator.page(not_answered_paginator.num_pages)

    if request.user.is_authenticated:
        context = {'base_template': os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html'),
                   'questions': question_page, 'loginPanel': os.path.join(COMPONENTS, 'widget_login_session.html'),
                   'notAnswered_': not_answered_}
        return render(request, 'apps/home/index.html', context)
    else:
        context = {'base_template': os.path.join(BASE_TEMPLATE, 'nonSessionComponents/navbar.html'),
                   'questions': question_page, 'loginPanel': os.path.join(COMPONENTS, 'widget_login.html'),
                   'notAnswered_': not_answered_}
        return render(request, 'apps/home/index.html', context)


def contac_us_view(request):
    if request.user.is_authenticated:
        contac_us_form = ContacUsForm(initial={'name': request.user.username, 'email': request.user.email})

        if contac_us_form.is_valid():
            contac_us_form.save()
            name = contac_us_form.cleaned_data.get('name')
            sweetify.success(request, '{} kaydiniz olusturuldu.'.format(name))
            contac_us_form = ContacUsForm()
        context = {'base_template': os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html'),
                   'contacUsForm': contac_us_form}
        return render(request, 'apps/home/contacUs.html', context)
    else:
        contac_us_form = ContacUsForm(request.POST or None)
        if contac_us_form.is_valid():
            contac_us_form.save()
            name = contac_us_form.cleaned_data.get('name')
            sweetify.success(request, '{} kaydiniz olusturuldu.'.format(name))
            contac_us_form = ContacUsForm()
        base_template = 'components/nonSessionComponents/navbar.html'
        context = {'base_template': base_template, 'contacUsForm': contac_us_form}
        return render(request, 'apps/home/contacUs.html', context)


def search_view(request):
    if request.user.is_authenticated:
        base_template = os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html')
        login_panel = os.path.join(COMPONENTS, 'widget_login_session.html')
    else:
        base_template = os.path.join(BASE_TEMPLATE, 'nonSessionComponents/navbar.html')
        login_panel = os.path.join(COMPONENTS, 'widget_login_session.html')

    question_list = QuestionModel.objects.all()
    article_list = ArticleModel.objects.all()
    user_list = UserModel.objects.all()
    query = request.GET.get('query')
    if query:
        question_query = question_list.filter(
            Q(questionTitle__icontains=query) |
            Q(questionContent__icontains=query)
        )

        article_query = article_list.filter(
            Q(articleTitle__icontains=query) |
            Q(articleContent__icontains=query)
        )

        user_query = user_list.filter(
            Q(username__icontains=query) |
            # Email sorgusu gizlilik ayaraına gore degısmeli
            # Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

        context = {'base_template': base_template, 'loginPanel': login_panel, 'QuestionQuery': question_query,
                   'ArticleQuery': article_query,
                   'UserQuery': user_query}
        return render(request, 'apps/home/search.html', context)


def change_color_view(request):
    pass


def handler404(request, exception):
    if request.user.is_authenticated:
        base_template = 'components/sessionComponents/sessionNavbar.html'
    else:
        base_template = os.path.join(BASE_TEMPLATE, 'nonSessionComponents/navbar.html')

    contex = {'base_template': base_template}
    return render(request, 'components/commonComponents/notfound.html', contex, locals())


def beta(request):
    user_agent = request.META['HTTP_USER_AGENT']
    context = {'user_agent': user_agent}
    return render(request, 'apps/home/beta.html', context)
