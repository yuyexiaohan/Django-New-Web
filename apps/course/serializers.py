#!/usr/bin/env python 
# coding=utf-8
# @Time : 2018/11/14
# @Author : achjiang
# @File : serializers.py
from rest_framework import serializers
from .models import Teacher


class TeacherSerializers(serializers.ModelSerializer):
    """教师序列化"""

    class Meta:
        model = Teacher
        fields = ("username", "jobtitle", "profile", "avatar")


"""
>>> from apps.course.serializers import TeacherSerializers
>>> serializer = TeacherSerializers()
>>> print(repr(serializer))
TeacherSerializers():
    username = CharField(max_length=100)
    jobtitle = CharField(max_length=100)
    profile = CharField(style={'base_template': 'textarea.html'})
    avatar = URLField(max_length=200)

"""
