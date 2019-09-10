from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """继承django模型的原有user"""

    def _create_user(self, telephone, username, password, **kwargs):
        """#1 创建通用类user"""
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, username, password, **kwargs):
        """user明确身份‘非superuser’"""
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        """创建超级用户"""
        kwargs['is_superuser'] = True
        return self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """user模型"""
    telephone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    is_active = models.BooleanField(default=True)
    gender = models.IntegerField(default=0)  # 0:代表未知，1：男，2：女
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)  # 这里的命名是规定好的，
    # user_img_url = models.URLField (default=None)

    # USERNAME_FIELD：这个属性是以后在使用authenticate
    # 进行验证的时候的字段
    USERNAME_FIELD = 'telephone'
    # 这个属性是用来，以后在命令行中使用createsuperuser命令
    # 的时候，会让你输入的字段，那么这里我们只要写一个username
    # 以后在创建超级管理员的时候，就会让你输入USERNAME_FIELD指定的字段
    # 现在USERNAME_FIELD指定的字段是telephone，以及password（这个字段你不写也会让你输入）
    REQUIRED_FIELDS = ['username']
    # 以后给某个用户发送邮箱的时候，就会使用这个属性指定的字段的值来发送
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


