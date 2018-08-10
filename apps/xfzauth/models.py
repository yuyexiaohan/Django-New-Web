# from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,BaseUserManager)
# from django.db import models
#
# class UserManager(BaseUserManager):
# 	def _create_user(self,telephone,username,password,**kwargs):
# 		user = self.model(telephone=telephone,username=username,**kwargs)
# 		user.set_password(password)
# 		user.save()
# 		return user
#
# 	def create_user(self,telephone,username,password,**kwargs):
# 		kwargs['is_superuser'] = False
# 		return self._create_user(telephone,username,password,**kwargs)
#
# 	def create_superuser(self,telephone,username,password,**kwargs):
# 		kwargs['is_superuser'] = True
# 		return self._create_user(telephone,username,password,**kwargs)
#
#
#
# class User(AbstractBaseUser,PermissionsMixin):
# 	telephone = models.CharField(max_length=11,unique=True)
# 	username = models.CharField(max_length=50)
# 	email = models.EmailField(unique=True)
# 	is_active = models.BooleanField(default=True)
# 	gender = models.IntegerField(default=0) # 0代表性别未确定，1代表男，2代表女
# 	date_joined = models.DateTimeField(auto_now=True)
#
# 	# USERNAME_FILED:这个属性是以后使用authenticate进行验证的时候的字段
# 	USERNAME_FIELD = 'telephone'
# 	# 这个属性是用来，后续命令中用到createsuperuser命令时，会让输入字段。
# 	# 那么这里我们只要写一个username以后创建超级管理员用户时，就会让你输
# 	# 入USERNAME_FIELD指定字段
# 	# 现在USERNAME_FIELD指定的字段telephone，以及password这两个字段，不写
# 	# 系统也会让你输入
# 	REQUIRED_FIELDS = ['usernme']
# 	# 以后给某个用户发邮箱的时候，就会用到这个属性指定的字段的值进行发送
# 	EMALL_FIELD = 'email'
#
# 	objects = UserManager()
#
# 	def get_full_name(self):
# 		return self.username
#
# 	def get_short_name(self):
# 		return self.username
#
# 	# User.objects.create_user()
# 	# User.objects.create_superuser()



# 老师代码

from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    ''''''
    def _create_user(self,telephone,username,password,**kwargs):
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone,username,password,**kwargs)

    def create_superuser(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = True
        return self._create_user(telephone,username,password,**kwargs)


class User(AbstractBaseUser,PermissionsMixin):
    telephone = models.CharField(max_length=11,unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True,null=True)
    is_active = models.BooleanField(default=True)
    gender = models.IntegerField(default=0) # 0:代表未知，1：男，2：女
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

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

