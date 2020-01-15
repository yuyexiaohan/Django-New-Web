#  定义User序列化
from rest_framework import serializers

from .models import User


class UserSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'telephone',
            'email',
            'date_joined',
            'is_staff',
            'is_active')
