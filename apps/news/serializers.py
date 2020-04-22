#  定义序列化,将一个模型序列化为一个json字段
from rest_framework import serializers
from .models import News, NewCategory, Comment
from apps.xfzauth.serializers import UserSerizlizer


class NewsCategorySerizlizer(serializers. ModelSerializer):
    """新闻分类序列化"""

    class Meta:
        model = NewCategory
        fields = ('id', 'name')


class NewsSerializer(serializers.ModelSerializer):
    # 当使用到到category时，从NewsCategorySerizlizer类中获取
    category = NewsCategorySerizlizer()
    author = UserSerizlizer()

    class Meta:
        model = News
        fields = (
            'id',
            'title',
            'desc',
            'thumbnail',
            'pub_time',
            'category',
            'author')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerizlizer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'pub_time')
