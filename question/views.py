import sweetify
import os
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datetime_safe import datetime
from linuxturkey.email import send_mail
from .forms import AskQuestionForm, AnswerForm, QuestionReport, EditAnswerForm, ReplyForm
from question.models import QuestionModel, AnswerModel, QuestionReportModel, FavoriteQuestionModel, ScoreModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.models import QuestionHistory, UserModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_TEMPLATE = os.path.join(BASE_DIR, 'templates/components/')
COMPONENTS = os.path.join(BASE_DIR, 'templates/components/commonComponents/')
SIDE_MENU = os.path.join(BASE_DIR, 'templates/components/sessionComponents/')
EMAIL_TEMPLATE = os.path.join(BASE_DIR, 'templates/components/email')


def ask_question_view(request):
    if request.user.is_authenticated:
        askquestion_form_ = AskQuestionForm(request.POST or None)
        if askquestion_form_.is_valid():
            form = askquestion_form_.save(commit=False)
            # form.slug = slugify(form.questionTitle)
            form.userID = request.user
            form.save()
            sweetify.success(request, 'Sorunuz oluşturuldu şimdi yönlediriliyorsunuz')
            return redirect('home:home')

        base_template = os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html')
        login_panel = os.path.join(COMPONENTS, 'widget_login_session.html')
        context = {'base_template': base_template, 'loginPanel': login_panel, 'AskQuestionForm': askquestion_form_}
        return render(request, 'apps/question/askQuestion.html', context)
    else:
        return redirect('user:login')


def show_question_view(request, slug):
    question = get_object_or_404(QuestionModel, slug=slug)
    question_id = question.id
    answer_counter = AnswerModel.objects.filter(questionID=question_id).count()
    favorite_counter = FavoriteQuestionModel.objects.filter(questionID=question_id).count()
    is_favorited = FavoriteQuestionModel.objects.filter(questionID=question_id, userID=request.user.id).exists()

    random_question = QuestionModel.objects.order_by('?')[:4]
    # TODO: Rastgele soru sorgusunu iyilestir

    # Answer Query
    answer = AnswerModel.objects.filter(questionID=question_id)
    best_answer_ = AnswerModel.objects.filter(questionID=question_id).values('bestAnswer')

    try:
        best_answer = best_answer_[0]['bestAnswer']
    except IndexError:
        best_answer = False

    answer_form_ = AnswerForm(request.POST or None)
    reply_form = ReplyForm(request.POST or None)
    question_report_form = QuestionReport(request.POST or None)

    if request.user.is_authenticated:
        base_template = os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html')
        login_panel = os.path.join(COMPONENTS, 'widget_login_session.html')
        # Kullanici Daha Once Raporlayip Raporlamadigini Kontrol Eder
        check_question_report = QuestionReportModel.objects.filter(reporterID=request.user,
                                                                   questionID=question_id).exists()
        QuestionHistory.objects.create(userID_id=request.user.id, questionID_id=question.id,
                                       ipAddress=request.META.get('REMOTE_ADDR'))

        question_history = QuestionHistory.objects.filter(userID_id=request.user.id,
                                                          questionID_id=question.id).order_by('-id')[:2]
        if question_history.exists():
            try:
                time_diff = question_history[0].historyDate - question_history[1].historyDate
                if time_diff.seconds > 600:
                    question.questionViewCounter += 1
                    QuestionModel.objects.filter(id=question.id).update(
                        questionViewCounter=question.questionViewCounter)
            except IndexError:
                question.questionViewCounter += 1
                QuestionModel.objects.filter(id=question.id).update(
                    questionViewCounter=question.questionViewCounter)

        # Cevaplama Sorgulama Baslangic
        if answer_form_.is_valid():
            form = answer_form_.save(commit=False)
            form.userID = request.user
            form.questionID = question
            form.bestAnswer = False
            form.save()
            redirect('question:showQuestion', question_id)
            # Cevaplama Sorgulama Bitis

        if question_report_form.is_valid() and check_question_report is True:
            sweetify.info(request, 'Daha önce raporlamışsın.', timer=2000)

        elif question_report_form.is_valid():
            report_form = question_report_form.save(commit=False)
            report_form.questionID = question
            report_form.reporterID = request.user
            report_form.save()
            sweetify.success(request, 'Şikayetiniz bize ulaştı. Topluluğumuzu daha düzenli hale getirmeye '
                                      'çalıştığınız için teşekkürler', timer=2000)
        context = {'base_template': base_template, 'question': question, 'answer': answer,
                   'AnswerCounter': answer_counter,
                   'loginPanel': login_panel,
                   'bestAnswer': best_answer,
                   'AnswerForm_': answer_form_,
                   'QuestionReportForm': question_report_form,
                   'CheckQuestionReport': check_question_report,
                   'randomQuestion': random_question,
                   'favorite_counter': favorite_counter,
                   'is_favorited': is_favorited
                   }
        return render(request, 'apps/question/showQuestion.html', context)
    else:
        base_template = os.path.join(BASE_TEMPLATE, 'nonSessionComponents/navbar.html')
        login_panel = os.path.join(COMPONENTS, 'widget_login.html')
        QuestionHistory.objects.create(questionID_id=question.id,
                                       ipAddress=request.META.get('REMOTE_ADDR'))

        question_history = QuestionHistory.objects.filter(questionID_id=question.id,
                                                          ipAddress=request.META.get('REMOTE_ADDR')).order_by('-id')[:2]
        if question_history.exists():
            try:
                time_diff = question_history[0].historyDate - question_history[1].historyDate
                if time_diff.seconds > 600:
                    question.questionViewCounter += 1
                    QuestionModel.objects.filter(id=question.id).update(
                        questionViewCounter=question.questionViewCounter)
            except IndexError:
                question.questionViewCounter += 1
                QuestionModel.objects.filter(id=question.id).update(
                    questionViewCounter=question.questionViewCounter)

        context = {'base_template': base_template, 'question': question, 'answer': answer,
                   'AnswerCounter': answer_counter,
                   'loginPanel': login_panel,
                   'bestAnswer': best_answer,
                   'AnswerForm_': answer_form_,
                   'ReplyForm_': reply_form,
                   'randomQuestion': random_question,
                   'favorite_counter': favorite_counter
                   }
        return render(request, 'apps/question/showQuestion.html', context)


def edit_question_view(request, question_id):
    base_template = os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html')
    login_panel = os.path.join(COMPONENTS, 'widget_login_session.html')

    if QuestionModel.objects.filter(userID_id=request.user.id, id=question_id).exists() is False:
        return redirect('home:home')

    question = get_object_or_404(QuestionModel, id=question_id)

    edit_form = AskQuestionForm(request.POST or None, instance=question)

    if edit_form.is_valid():
        edit_forn_ = edit_form.save(commit=False)
        edit_forn_.questionEditDate = datetime.now()
        edit_forn_.save()
        sweetify.success(request, 'Sorunuz Güncellendi')
        return redirect('home:home')

    context = {
        'base_template': base_template,
        'loginPanel': login_panel,
        'editForm': edit_form
    }

    return render(request, 'apps/question/editQuestion.html', context)


def question_delete_view(request):
    question_id = request.GET.get('id')
    question_model = QuestionModel.objects.filter(pk=question_id, userID=request.user.id)
    if question_model.exists() is True:
        question_model.delete()
        data = 'E001'
    else:
        data = 'E002'

    data = {
        'status': data
    }
    return JsonResponse(data)


def edit_answer_view(request, answer_id):
    base_template = os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html')
    login_panel = os.path.join(COMPONENTS, 'widget_login_session.html')

    if AnswerModel.objects.filter(userID_id=request.user.id, id=answer_id).exists() is False:
        return redirect('home:home')

    answer = get_object_or_404(AnswerModel, id=answer_id)

    edit_form = EditAnswerForm(request.POST or None, instance=answer)

    if edit_form.is_valid():
        edit_form.save()
        sweetify.success(request, 'Cevabınız Güncellendi')
        return redirect('home:home')

    context = {
        'base_template': base_template,
        'loginPanel': login_panel,
        'editForm': edit_form
    }

    return render(request, 'apps/question/editAnswer.html', context)


def delete_answer_view(request):
    answer_id = request.GET.get('id')
    answer = AnswerModel.objects.filter(userID=request.user.id, id=answer_id)

    if answer.exists() is True:
        answer.delete()
        status = 'E001'
    else:
        status = 'E002'

    data = {
        'status': status
    }
    return JsonResponse(data)


def add_question_favorite_view(request):
    username = request.user.id
    question_id = request.GET.get('id')

    if FavoriteQuestionModel.objects.filter(userID_id=username, questionID_id=question_id).exists():
        FavoriteQuestionModel.objects.filter(userID_id=username, questionID_id=question_id).delete()
        data = False
        count = FavoriteQuestionModel.objects.filter(userID_id=username, questionID_id=question_id).count()
    else:
        FavoriteQuestionModel.objects.create(userID_id=username, questionID_id=question_id)
        data = True
        count = FavoriteQuestionModel.objects.filter(userID_id=username, questionID_id=question_id).count()

    data_ = {
        'status_': data,
        'counter_': count
    }

    return JsonResponse(data_)


def add_yes_vote_view(request):
    data = {'count': 0}
    answer_id = request.GET.get('answerID')

    answer = get_object_or_404(AnswerModel, id=answer_id)
    if not ScoreModel.objects.filter(user=request.user, answer=answer).exists():
        answer.score += 1
        ScoreModel.objects.create(user=request.user, answer=answer, score_status=1)
        answer.save()

    elif ScoreModel.objects.get(user=request.user, answer=answer).score_status == -1:
        scm = ScoreModel.objects.get(user=request.user, answer=answer)
        answer.score += 1
        scm.score_status += 1
        answer.save()
        scm.save()
    elif ScoreModel.objects.get(user=request.user, answer=answer).score_status == 0:
        scm = ScoreModel.objects.get(user=request.user, answer=answer)
        answer.score += 1
        scm.score_status += 1
        answer.save()
        scm.save()

    count = answer.score
    data.update({'count': count})

    return JsonResponse(data)


def add_no_vote_view(request):
    data = {'count': 0}
    answer_id = request.GET.get('answerID')
    answer = AnswerModel.objects.get(pk=answer_id)

    if not ScoreModel.objects.filter(user=request.user, answer=answer).exists():
        answer.score -= 1
        ScoreModel.objects.create(user=request.user, answer=answer, score_status=-1)
        answer.save()

    elif ScoreModel.objects.get(user=request.user, answer=answer).score_status == 0:
        answer.score -= 1
        answer.save()
        scm = ScoreModel.objects.get(user=request.user, answer=answer)
        scm.score_status -= 1
        scm.save()
    elif ScoreModel.objects.get(user=request.user, answer=answer).score_status == 1:
        answer.score -= 1
        answer.save()
        scm = ScoreModel.objects.get(user=request.user, answer=answer)
        scm.score_status -= 1
        scm.save()

    count = answer.score
    data.update({'count': count})

    return JsonResponse(data)


def add_answer_view(request):
    username = request.user.id
    answer = request.POST['answer']
    question_id = request.POST['questionID']

    if answer is not "":
        answer_status = AnswerModel.objects.create(userID_id=username, questionID_id=question_id, answer=answer)
        question = QuestionModel.objects.get(id=question_id)

        user_model = UserModel.objects.get(pk=username)
        username_mail = user_model.username
        context = {'repliedTo': username_mail, 'question': question.questionTitle}

        if question.emailNotifications is True:
            send_mail(question.userID.email, 'Sorunuza Cevap Geldi', os.path.join(EMAIL_TEMPLATE, 'replied.html'),
                      **context)

    else:
        answer_status = AnswerModel.objects.filter(questionID_id=question_id)

    if answer_status:
        data = list(AnswerModel.objects.filter(questionID_id=question_id).values())
        count = AnswerModel.objects.filter(questionID=question_id).count()
    else:
        data = False
        count = AnswerModel.objects.filter(questionID=question_id).count()

    data = {
        'data': data,
        'count_': count,
        'answer_': answer
    }

    return JsonResponse(data)


def best_answer_view(request):
    user_id = request.user.id
    answer_id = request.GET.get('answerID')

    # E001 -> Object does not exit
    answer_id = AnswerModel.objects.get(pk=answer_id)

    answer_query = AnswerModel.objects.filter(questionID=answer_id.questionID).values_list('questionID',
                                                                                           flat=True).distinct()
    check_best_answer = answer_query.filter(bestAnswer=True)
    if check_best_answer.exists():
        check_best_answer.update(bestAnswer=False)
        AnswerModel.objects.filter(id=answer_id.id).update(bestAnswer=True)

        data = 'E002'
    else:
        AnswerModel.objects.filter(id=answer_id.id).update(bestAnswer=True)
        data = 'E000'

    data = {
        'status': data}

    return JsonResponse(data)


def question_category_view(request, category_id):
    questions = QuestionModel.objects.filter(categoryID=category_id)

    question_paginator = Paginator(questions, 20)
    page = request.GET.get('page')

    try:
        question_page = question_paginator.get_page(page)
    except PageNotAnInteger:
        question_page = question_paginator.page(1)
    except EmptyPage:
        question_page = question_paginator.page(question_paginator.num_pages)

    if request.user.is_authenticated:
        context = {'base_template': os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html'),
                   'questions': question_page,
                   'loginPanel': os.path.join(COMPONENTS, 'widget_login_session.html')}
        return render(request, 'apps/question/questionCategory.html', context)
    else:
        context = {'base_template': os.path.join(BASE_TEMPLATE, 'nonSessionComponents/navbar.html'),
                   'questions': question_page,
                   'loginPanel': os.path.join(COMPONENTS, 'widget_login.html')}
        return render(request, 'apps/question/questionCategory.html', context)


def add_reply_view(request):
    pass
