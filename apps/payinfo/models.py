from django.db import models
from shortuuidfield import ShortUUIDField  # 导入


class Payinfo(models.Model):
    price = models.FloatField()
    # 链接
    path = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    profile = models.CharField(max_length=100)

# def get_user():
# 	from apps.xfzauth.models import User
# 	return User.objects.filter()


class PayinfoOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)  # 不是自增长id
    payinfo = models.ForeignKey('Payinfo', on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    # DO_NOTHING：在django中，不会做任何的处理。完全看数据库的关系
    buyer = models.ForeignKey('xfzauth.User', on_delete=models.DO_NOTHING)
    # 设置为默认值时，就会从定义的函数中取值
    # buyer = models.ForeignKey('xfzauth.User',on_delete=models.SET_DEFAULT,default=get_user())

    pub_time = models.DateTimeField(auto_now_add=True)
    # 1:代表的时支付宝支付，2：代表的时微信支付
    istype = models.SmallIntegerField(default=0)
    # 1:代表的时未支付。2：代表的时已支付
    status = models.SmallIntegerField(default=1, null=True)
