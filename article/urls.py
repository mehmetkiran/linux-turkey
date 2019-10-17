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

app_name = 'article'

urlpatterns = [
    path('home/', blog_home_view, name='home'),
    path('read/<int:article_id>/', read_article_view, name='articleRead'),
    path('showArticle/<int:category_id>/', show_category_view, name='showArticle'),
    path('addArticle/', create_article_view, name='addArticle'),
    path('createpdf/', create_pdf_view, name='createPDF'),

]
