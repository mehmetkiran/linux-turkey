from rest_framework import serializers

from article.models import ArticleModel, CommentModel
from question.models import QuestionModel
from user.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.StringRelatedField(many=True)

    class Meta:
        model = QuestionModel
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    answer = serializers.StringRelatedField(many=True)

    class Meta:
        model = ArticleModel
        fields = '__all__'
