from django.db import models


class NewCategory(models.Model):
	"""新闻分类表"""
	name =  models.CharField(max_length=100)


# aware time：清醒的时间（清醒的知道自己这个时间代表的是哪个时区的）
# navie time：幼稚的时间（不知道自己的时间代表的是哪个时区）


class News(models.Model):
	"""新闻表"""
	title = models.CharField(max_length=200)  # 题目
	desc = models.CharField(max_length=200)  # 描述
	thumbnail = models.URLField()  # 缩略图链接
	content = models.TextField()  # 发布内容
	pub_time = models.DateTimeField(auto_now=True)  # 发布时间，设置为当前时间
	# 关联外键
	category = models.ForeignKey("NewCategory", on_delete=models.SET_NULL, null=True)
	# 默认情况下，category不能为空，null默认是为false，如果我们设置它为空，就需要将null配置成True（允许为空）
	author = models.ForeignKey("xfzauth.User", on_delete=models.SET_NULL, null=True)

	class Meta:
		# 以后News.objects提出数据的时候，就会按照列表指定的字段排序
		# 如果不加负号，就会默认按照从小到大正序排序
		# 如果加负号，就会按照从大到小倒序排序
		ordering = ['-pub_time']


class Comment(models.Model):
	"""评论内容"""
	content = models.TextField()
	pub_time = models.DateTimeField(auto_now_add=True)
	news = models.ForeignKey("News", on_delete=models.CASCADE, related_name='comments')
	# 定义一个related——name(别名)
	author = models.ForeignKey("xfzauth.User", on_delete=models.CASCADE)

	class Meta:
		ordering = ['-pub_time']


class Banner(models.Model):
	"""轮播图"""
	image_url = models.URLField()  # 定义一个图片链接的属性
	priority = models.IntegerField(default=0)  # 创建一个优先级属性
	link_to = models.URLField()  # 图片a标签的超链接属性
	pub_time = models.DateTimeField(auto_now_add=True)  # 定义一个发布事件，设置事件自动设置为当前时间

	class Meta:
		ordering = ['-priority']
