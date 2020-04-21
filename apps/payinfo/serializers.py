#!/usr/bin/env python 
# coding=utf-8
# @Time : 2020/4/21
# @Author : achjiang
# @File : serializers.py

from rest_framework import serializers
from .models import Payinfo


class PayInfoSerializers(serializers.ModelSerializer):
    """付费信息序列化"""

    class Meta:
        model = Payinfo
        fields = ['id', 'title', 'profile', 'price']
