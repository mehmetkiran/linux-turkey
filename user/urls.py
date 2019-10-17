"""linuxturkey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('editProfile/', edit_profile_view, name='editProfile'),
    path('changePassword/', change_password_view, name='changePassword'),
    path('showProfile/<int:user_id>/', show_profile_view, name='showProfile'),
    path('logout', user_logout_view, name='logout'),
    path('loginHistory/', login_history_view, name='loginHistory'),
    path('verify/', verify_user_view, name='verify'),
    path('newPassword/', new_password_view, name='forgotPassword'),
    path('newPasswordAjax', new_password_view_ajax, name='forgotPasswordAjax'),
    path('verifyAjax/', verify_user_ajax, name='verifyAjax'),
    path('confirmCode/', send_code_view, name='sendCode'),
    path('sendCodeAjax/', send_code_ajax, name='sendCodeAjax'),
    path('questionHistory/', question_history_view, name='questionHistory'),
    path('notificationSettings/', notification_settings_view, name='notificationSettings')

]
