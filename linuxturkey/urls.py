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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home.views import home_view
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('questions', views.QuestionViewSet)
router.register('articles', views.ArticleViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('home/', include('home.urls', namespace='home')),
    path('user/', include('user.urls', namespace='user')),
    path('article/', include('article.urls', namespace='article')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('question/', include('question.urls', namespace='question')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'home.views.handler404'
