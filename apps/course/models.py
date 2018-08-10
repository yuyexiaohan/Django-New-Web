from django.db import models


class CourseCategory(models.Model):
	'''定义一个课程分类的模型'''
	name = models.CharField(max_length=100) # 课程名称


class Teacher(models.Model):
	'''定义一个老师模型'''
	username = models.CharField(max_length=100) # 老师名称
	jobtitle = models.CharField(max_length=100) # 职位
	profile = models.TextField() # 简介
	avatar = models.URLField() # 图像


class Course(models.Model):
	'''定义一个课程发布的模型'''
	title = models.CharField(max_length=100)
	video_url = models.URLField() # 视频链接
	cover_url = models.URLField() # 封面图片链接
	price = models.FloatField() # 课程价格
	duration = models.IntegerField() # 持续时间代表的是秒
	profile = models.TextField() # 课程简介
	pub_time = models.DateTimeField(auto_now_add=True) # 课程发布时间，加入当前时间
	# 外键关联课程分类表
	category = models.ForeignKey('CourseCategory',on_delete=models.DO_NOTHING)
	# 外键关联老师表
	teacher = models.ForeignKey('Teacher',on_delete=models.DO_NOTHING)


class CourseOrder(models.Model):
	'''创建订单表'''
	pub_time = models.DateTimeField(auto_now_add=True)
	amount = models.FloatField() # 课程价格
	# 1：代表的是未支付。2：代表的是支付成功
	status = models.SmallIntegerField()
	course = models.ForeignKey("Course",on_delete=models.DO_NOTHING)
	buyer = models.ForeignKey("xfzauth.User",on_delete=models.DO_NOTHING)
	# 0:代表未知。1:代表支付宝支付。2：代表微信支付
	istype = models.SmallIntegerField(default=0)



'''
	对于修改模型内容，例如表结构时，可能之前已经存在一些数据，这样直接添加一个表属性时，会在执行makemigrations appname时报错。
	可以通过，在定义该变量后面，申明null=True
'''


