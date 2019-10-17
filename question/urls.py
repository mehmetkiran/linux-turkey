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

app_name = 'question'

urlpatterns = [
    path('askQuestion', ask_question_view, name='askQuestion'),
    path('editQuestion/<int:question_id>/', edit_question_view, name='editQuestion'),
    path('addFavorite/', add_question_favorite_view, name='addFavorite'),
    path('yesVote/', add_yes_vote_view, name='yesVote'),
    path('noVote/', add_no_vote_view, name='noVote'),
    path('bestAnswer/', best_answer_view, name='bestAnswer'),
    path('answer/', add_answer_view, name='addAnswer'),
    path('questionCategory/<int:category_id>/', question_category_view, name='questionCategory'),
    path('deleteQuestion/', question_delete_view, name='deleteQuestion'),
    path('editAnswer/<int:answer_id>/', edit_answer_view, name='editAnswer'),
    path('deleteAnswer/', delete_answer_view, name='deleteAnswer'),
    path('showQuestion/<slug:slug>/', show_question_view, name='showQuestion'),
    path('addReply', add_reply_view, name='addReply')

]
