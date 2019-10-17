from rest_framework import viewsets

from .serializer import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = QuestionModel.objects.all().order_by('-id')
    serializer_class = QuestionSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = ArticleModel.objects.all().order_by('-id')
    serializer_class = ArticleSerializer
