import os
import django
import sweetify
from datetime import timedelta
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from linuxturkey.email import send_mail
from question.models import AnswerModel, FavoriteQuestionModel
from .forms import *
from django.utils import timezone
from .models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_TEMPLATE = os.path.join(BASE_DIR, 'templates/components/')
COMPONENTS = os.path.join(BASE_DIR, 'templates/components/commonComponents/')
SIDE_MENU = os.path.join(BASE_DIR, 'templates/components/sessionComponents/')
EMAIL_TEMPLATE = os.path.join(BASE_DIR, 'templates/components/email/')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home:home')
    else:
        login_form = UserLoginForm(request.POST or None)
        ip_address = request.META.get('REMOTE_ADDR')
        browser = request.user_agent.browser.family
        if request.POST.get('submit') == 'login_':
            #  Login Form

            if login_form.is_valid():
                username = login_form.cleaned_data.get('username_')
                # geo_ip = GeoIP2()
                password = login_form.cleaned_data.get('password_')
                # city = geo_ip.city(ip_address)
                user = authenticate(username=username, password=password)
                login(request, user)
                UserLoginHistory.objects.create(userID_id=request.user.id, ipAddress=ip_address,
                                                userAgent=request.META['HTTP_USER_AGENT'], browser=browser,
                                                status=1)
                return redirect('home:home')

        context = {'base_template': os.path.join(BASE_TEMPLATE, 'nonSessionComponents/navbar.html'),
                   'LoginForm': login_form}
        return render(request, 'apps/user/login.html', context)


def edit_profile_view(request):
    if request.user.is_authenticated:
        edit_user = get_object_or_404(UserModel, id=request.user.id)

        user_profile_change = UserProfileChangeForm(request.POST or None, request.FILES or None,
                                                    initial={'email': request.user.email,
                                                             'userAbout': request.user.userAbout,
                                                             'userCountry': request.user.userCountry,
                                                             'userFacebook': request.user.userFacebook,
                                                             'userTwitter': request.user.userTwitter,
                                                             'userLinkedin': request.user.userLinkedin,
                                                             'userWebsite': request.user.userWebsite},
                                                    instance=edit_user)

        if user_profile_change.is_valid():
            form = user_profile_change.save(commit=False)
            form.userID = request.user
            form.save()
            sweetify.success(request, 'Ayarlar başarıyla güncellendi.')
            redirect('user:editProfile')

        context = {'base_template': os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html'),
                   'loginPanel': os.path.join(COMPONENTS, 'widget_login_session.html'),
                   'UserProfileChange': user_profile_change}
        return render(request, 'apps/user/editProfile.html', context)
    else:
        return redirect('user:login')


def change_password_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                sweetify.success(request, 'Parolanız güncellendi!')
                return redirect('user:changePassword')
            else:
                sweetify.error(request, 'Hataları düzeltin!.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'apps/user/changePassword.html',
                      {'base_template': os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html'),
                       'form': form
                       })
    else:
        return redirect('home:home')


def show_profile_view(request, user_id):
    start_date = timezone.now()
    end_date30 = start_date - timedelta(30)
    end_date1 = start_date - timedelta(1)

    user_profile = get_object_or_404(UserModel, id=user_id)
    user_question_page = QuestionModel.objects.filter(userID=user_id)

    user_question_paginator = Paginator(user_question_page, 10)
    question_page = request.GET.get('questionPage')

    try:
        user_question = user_question_paginator.page(question_page)
    except PageNotAnInteger:
        user_question = user_question_paginator.page(1)
    except EmptyPage:
        user_question = user_question_paginator.page(user_question_paginator.num_pages)

    user_question_count = user_question_page.count()

    user_answer_page = AnswerModel.objects.filter(userID=user_id)

    user_answer_paginator = Paginator(user_answer_page, 10)
    answer_page = request.GET.get('answerPage')

    try:
        user_answer = user_answer_paginator.get_page(answer_page)
    except PageNotAnInteger:
        user_answer = user_answer_paginator.page(1)
    except EmptyPage:
        user_answer = user_answer_paginator.page(user_answer_paginator.num_pages)

    user_answer_count = user_answer_page.count()
    user_best_answer = AnswerModel.objects.filter(userID=user_id, bestAnswer=1).count()

    user_question_30days = QuestionModel.objects.filter(userID=user_id,
                                                        questionCreateDate__range=[end_date30, start_date]).count()
    user_question_1day = QuestionModel.objects.filter(userID=user_id,
                                                      questionCreateDate__range=[end_date1, start_date]).count()

    user_answer_30days = AnswerModel.objects.filter(userID=user_id, answerDate__range=[end_date30, start_date]).count()
    user_answer_1day = AnswerModel.objects.filter(userID=user_id, answerDate__range=[end_date1, start_date]).count()

    user_favorite_question_page = FavoriteQuestionModel.objects.filter(userID=user_id)
    user_favorite_question_count = user_favorite_question_page.count()

    user_favorite_question_paginator = Paginator(user_favorite_question_page, 10)
    favorite_page = request.GET.get('favoritePage')

    try:
        user_favorite_question = user_favorite_question_paginator.get_page(favorite_page)
    except PageNotAnInteger:
        user_favorite_question = user_favorite_question_paginator.page(1)
    except EmptyPage:
        user_favorite_question = user_favorite_question_paginator.page(user_favorite_question_paginator.num_pages)

    if request.user.is_authenticated:
        context = {'base_template': os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html'),
                   'userProfile': user_profile, 'userQuestion': user_question,
                   'userAnswer': user_answer, 'userBestAnswer': user_best_answer,
                   'userQuestion30Days': user_question_30days, 'userQuestion1Day': user_question_1day,
                   'userAnswer30Days': user_answer_30days,
                   'userAnswer1Day': user_answer_1day,
                   'userFavoriteQuestion': user_favorite_question,
                   'userFavoriteQuestionCount': user_favorite_question_count,
                   'userQuestionCount': user_question_count,
                   'userAnswerCount': user_answer_count,
                   'loginPanel': os.path.join(COMPONENTS, 'widget_login_session.html')
                   }
        return render(request, 'apps/user/showProfile.html', context)
    else:
        context = {'base_template': os.path.join(BASE_TEMPLATE, 'nonSessionComponents/navbar.html'),
                   'userProfile': user_profile, 'userQuestion': user_question,
                   'userAnswer': user_answer, 'userBestAnswer': user_best_answer,
                   'userQuestion30Days': user_question_30days, 'userQuestion1Day': user_question_1day,
                   'userAnswer30Days': user_answer_30days,
                   'userAnswer1Day': user_answer_1day,
                   'userFavoriteQuestion': user_favorite_question,
                   'userFavoriteQuestionCount': user_favorite_question_count,
                   'userQuestionCount': user_question_count,
                   'userAnswerCount': user_answer_count,
                   'loginPanel': os.path.join(COMPONENTS, 'widget_login.html')
                   }
        return render(request, 'apps/user/showProfile.html', context)


def register_view(request):
    base_template = 'components/nonSessionComponents/navbar.html'
    register_form = UserRegisterForm(request.POST or None)
    if register_form.is_valid():
        user = register_form.save(commit=False)
        password = register_form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        authenticate(username=user.username, password=password)

        user_id = UserModel.objects.get(email=user.email)
        UserVerifyModel.objects.create(userID_id=user_id.id)
        verify_model = UserVerifyModel.objects.get(userID_id=user_id.id)

        kwargs = {
            'verifyCode': str(verify_model.publicKey)
        }
        send_mail(user.email, 'Hesabınızı Onaylayın', os.path.join(EMAIL_TEMPLATE, 'newUser.html'), **kwargs)

    context = {'base_template': base_template, 'registerForm': register_form}
    return render(request, 'apps/user/register.html', context)


def verify_user_view(request):
    base_template = os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html')
    context = {'base_template': base_template}

    if UserModel.objects.get(id=request.user.id).isVerified == 1:
        return render(request, 'apps/user/verified.html', context)
    else:
        return render(request, 'apps/user/verify.html', context)


def verify_user_ajax(request):
    public_key = request.GET.get('publicKey')

    public_key_ = UserVerifyModel.objects.get(userID_id=request.user.id).publicKey
    if public_key == str(public_key_):
        UserModel.objects.filter(id=request.user.id).update(isVerified=1)
        data = True

    else:
        data = False

    data = {
        'status_': data
    }
    return JsonResponse(data)


def login_history_view(request):
    if request.user.is_authenticated:
        login_history = UserLoginHistory.objects.filter(userID_id=request.user.id).order_by('-loginID')

        context = {'base_template': os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html'),
                   'loginHistory': login_history,
                   'sideMenu': os.path.join(SIDE_MENU, 'editProfileSideMenu.html'),
                   }
        return render(request, 'apps/user/loginHistory.html', context)
    else:
        return redirect('user:login')


def user_logout_view(request):
    logout(request)
    return redirect('home:home')


def new_password_view(request):
    base_template = os.path.join(BASE_TEMPLATE, 'nonSessionComponents/navbar.html')
    context = {'base_template': base_template}

    return render(request, 'apps/user/newPassword.html', context)


def new_password_view_ajax(request):
    email = request.GET.get('email')
    user = UserModel.objects.filter(email=email)
    forgot_password = ForgotPasswordModel.objects.filter(userID_id__email=email)

    # Status Code
    # E001 -> User not exists
    # E002 -> User exists and recovery key not exists
    # E003 -> User exists and recovery key exists
    # E004 -> Unknown Error

    if user.exists() is False:
        status_code = 'E001'
    elif user.exists() is True and forgot_password.exists() is False:
        user_id = UserModel.objects.get(email=email)
        if forgot_password.exists():
            forgot_password.delete()
            ForgotPasswordModel.objects.create(userID_id=user_id)
            forgot_password_p = ForgotPasswordModel.objects.get(userID_id__email=email)
        else:
            ForgotPasswordModel.objects.create(userID_id=user_id)
            forgot_password_p = ForgotPasswordModel.objects.get(userID_id__email=email)

        kwargs = {'username': user_id.username, 'verifyCode': forgot_password_p.publicKey, 'email': email}
        send_mail(email, 'Parola Sıfırlama', os.path.join(EMAIL_TEMPLATE, 'revoveryPassword.html'), **kwargs)
        status_code = 'E002'
    elif user.exists() is True and forgot_password.exists() is True:
        user_id = UserModel.objects.get(email=email)
        if forgot_password.exists():
            forgot_password.delete()
            ForgotPasswordModel.objects.create(userID_id=user_id)
            forgot_password_p = ForgotPasswordModel.objects.get(userID_id__email=email)
        else:
            ForgotPasswordModel.objects.create(userID_id=user_id)
            forgot_password_p = ForgotPasswordModel.objects.get(userID_id__email=email)

        kwargs = {'username': user_id.username, 'verifyCode': forgot_password_p.publicKey, 'email': email}
        send_mail(email, 'Parola Sıfırlama', os.path.join(EMAIL_TEMPLATE, 'revoveryPassword.html'), **kwargs)
        status_code = 'E002'
    else:
        status_code = 'E004'

    data = {
        'status': status_code
    }

    return JsonResponse(data)


def send_code_view(request):
    base_template = os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html')

    context = {'base_template': base_template}

    return render(request, 'apps/user/verifyCode.html', context)


def send_code_ajax(request):
    email = request.GET.get('email')
    public_key = request.GET.get('publicKey')

    try:
        if not ForgotPasswordModel.objects.filter(userID_id__email=email, publicKey=public_key).exists():

            status = 'E001'

        else:
            user = UserModel.objects.get(email__exact=email)
            username = user.username
            password = UserModel.objects.make_random_password()
            user.set_password(password)
            user.save()
            kwargs = {'username': username, 'password': password}
            send_mail(email, 'Yeni Parolaniz Hazir', os.path.join(EMAIL_TEMPLATE, 'newPassword.html'), **kwargs)
            status = 'E002'

        data = {
            'status': status
        }
        return JsonResponse(data)

    except django.core.exceptions.ValidationError:
        data = {
            'status': 'E003'
        }
        return JsonResponse(data)


def question_history_view(request):
    if request.user.is_authenticated:
        question_history = QuestionHistory.objects.filter(userID_id=request.user.id)

        context = {'base_template': os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html'),
                   'sideMenu': os.path.join(SIDE_MENU, 'editProfileSideMenu.html'),
                   'questionHistory': question_history}
        return render(request, 'apps/user/questionHistory.html', context)
    else:
        return redirect('user:login')


def notification_settings_view(request):
    if request.user.is_authenticated:

        context = {'base_template': os.path.join(BASE_TEMPLATE, 'sessionComponents/sessionNavbar.html'),
                   # 'form': form,
                   'sideMenu': os.path.join(SIDE_MENU, 'editProfileSideMenu.html'),
                   }

        return render(request, 'apps/user/notificationSettings.html', context)
    else:
        return redirect('user:login')
