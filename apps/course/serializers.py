#!/usr/bin/env python 
# coding=utf-8
# @Time : 2019/11/14
# @Author : achjiang
# @File : serializers.py
from rest_framework import serializers
from .models import Teacher


class TeacherSerializers(serializers):
    """教师序列化"""

    class Meta:
        models = Teacher
        fields = ("id", "username", "jobtitle", "profile", "avatar")
