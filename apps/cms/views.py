from django.shortcuts import render,redirect,reverse
from django.contrib.admin.views.decorators import staff_member_required # 导入django自带的确定是否登陆和是否是工作人员的装饰器，后面可以跟重定向的url
from django.views.generic import View # 使用类定义函数时，变量需要引入该模块
from django.views.decorators.http import require_POST,require_GET # 限制函数，只能使用post的请求，才能访问某个函数
from apps.news.models import NewCategory,News,Banner # 导入对应的数据库表单
from utils import restful  # 引入自定义的浏览器返回的错误信息文件
from .forms import EditNewsCategoryForm,WriteNewsForm,AddBanner,EditBannerForm,EditNewsForm # 导入对应的forms表单，用于与数据库表单数据关联
from django.conf import settings
import os,qiniu
from django.contrib.auth.decorators import login_required # 导入登录验证函数
from django.utils.decorators import method_decorator # 验证登录才能访问函数的装饰器
from django.core.paginator import Paginator
from datetime import datetime # 获取时间参数模块
from urllib import parse # 导入url函数
from django.contrib.auth.decorators import permission_required # 可以在该模块后给出一个条件，这样就可以要求对应的权限
from apps.xfzauth.decorators import xfz_permission_required

'''
# 定义一个cms管理的视图函数，返回一个cms管理界面
'''
# 调用staff_member_required函数来验证staff处的值是否为Ture，不为真就跳转到login_url='...'对应的链接。如果为真则执行后面的函数
@staff_member_required(login_url='/') # 这里跳转到首页
def index(request):
	category = NewCategory.objects.first ()
	# 快速增加测试新闻数据
	# for i in range(20):
	# 	title = '标题%s'%i
	# 	content = '内容%s'%i
	# 	desc = '描述信息%s'%i
	# 	thumbnail = '描述信息%s'%i
	# 	News.objects.create(title=title,content=content,desc=desc,thumbnail=thumbnail,category=category,author=request.user)
	return render(request,'cms/index.html')


'''定义一个新闻列表管理页面，使用类的方式构建函数便于继承相关的方法'''
# method_decorator是一个将装饰器函数转换为装饰器方法的，参数1：装饰器，参数2：
@method_decorator([xfz_permission_required(News)],name='dispatch')
class NewsList(View):
	def get(self,request):
		page = int (request.GET.get ('p', 1))  # 获取当前所在页数
		start = request.GET.get('start') # 通过前端的标签名获取值
		end = request.GET.get('end')
		title = request.GET.get('title')
		category_id = int(request.GET.get('category',0))

		# newses = News.objects.select_related ('category', 'author').all () # 获取所有新闻分类及作者
		newses = News.objects.select_related ('category', 'author')

		# 过滤出指定时间内的新闻
		if start and end:
			start_date = datetime.strptime(start,'%Y/%m/%d')
			end_date = datetime.strptime(end,'%Y/%m/%d')
			newses = newses.filter(pub_time__range=(start_date,end_date))

		# 过滤标题中包含指定关键字的新闻
		if title:
			newses = newses.filter(title__icontains=title) # i指忽略大小写，contains指包含

		# 过滤对应分类的新闻
		if category_id != 0:
			newses = newses.filter(category=category_id)
			print('分类名称：%s'%category_id,'新闻数量%s'%len(newses))


		paginator = Paginator (newses, 2)  # 将获取的新闻内容按照每页2篇的形式进行分页
		page_obj = paginator.page (page)  # 获取对应分页的数据
		categories = NewCategory.objects.all ()

		# 通过分页函数返回分页数据，获取每一页的数据
		pagination_data = self.get_pagination_data(paginator,page_obj)

		'''查询内容组成的查询url是否应该带'''
		# 方法1：
		# if (start and end) or title or category_id!=0 :
		# 	url_query = '&' + parse.urlencode ({
		# 		'start': start,
		# 		'end': end,
		# 		'title': title,
		# 		'category': category_id
		# 	})
		# else:
		# 	url_query = ''
		# 方法2：
		if start or end or title or category_id :
			url_query = '&' + parse.urlencode ({
				'start': start,
				'end': end,
				'title': title,
				'category': category_id
			})
		else:
			url_query = ''

		context = {
			'categories': categories,
			'paginator': paginator,
			'page_obj': page_obj,
			'newses': page_obj.object_list,  # 获取该页数据的内容
			'title':title,
			'start':start,
			'end':end,
			'category_id':category_id,
			# 查询内容url
			'url_query':url_query
		}
		print(context['url_query']) # 打印测试输出的是否是我们查询内容
		context.update(pagination_data)
		return render (request, 'cms/news_list.html', context=context)

	###定义一个分页函数
	# < 1...5,6,7,8,9...13 >基本模式，即选中页前后留出2页，多出的用...代替。当选择最前或最后前后两页包含或者临近第一页或最后一页，那么取消显示...
	def get_pagination_data(self,paginator,page_obj,around_count=1):
		current_page = page_obj.number #获取当前页码
		num_pages = paginator.num_pages

		# 左侧是否应该显示三个点
		left_has_more = False

		# 右侧是否应该显示三个点
		right_has_more = False

		# 左侧显示页
		# 判断当前页数小于需要展示页数+2时，不显示三个点
		l_start = current_page - around_count  # 左侧的开始页码数
		l_end = current_page  # 右侧结束页码数
		if current_page <= around_count + 2:
			left_pages = range(1,l_end)
		else:
			left_has_more = True
			left_pages = range(l_start,l_end)

		# 右侧显示页
		r_start = current_page + 1
		r_end = current_page + around_count +1  # ? 说绝对位置是是这个位置+1?
		if current_page >= num_pages - around_count-1:
			right_pages = range(r_start,num_pages+1)
		else:
			right_has_more = True
			right_pages = range(r_start,r_end)
		return {
			'left_pages':left_pages,
			'right_pages':right_pages,
			'left_has_more':left_has_more,
			'right_has_more':right_has_more,
			'num_pages':num_pages,
			'current_page':current_page
		}





'''
# 定义一个写入页面函数，并返回一个编辑界面
# 在编辑界面中获取页面数据并出入数据库
'''
#加入装饰器验证是否登录，登录执行该函数，未登录直接跳转到对应的url中
@method_decorator([login_required(login_url='/account/login/'),xfz_permission_required(News)],name='dispatch')
# dispatch 是什么方法？
class WriteNewsView(View):
	def get(self,request):
		context = {
			'categories':NewCategory.objects.all()
		}
		return render(request,'cms/write_news.html',context=context)
	# 写一个获取数据请求函数，应该考虑设计一张表来对数据进行验证
	def post(self,request):
		form = WriteNewsForm(request.POST)
		if form.is_valid():
		# cleaned_data：这个属性，必须要调用is_valid后，
		# 如果验证通过了才会生成这个属性，否则没有这个属性
			# 获取表单中的各个数据
			title = form.cleaned_data.get('title')
			desc = form.cleaned_data.get('desc')
			thumbnail = form.cleaned_data.get('thumbnail')
			content = form.cleaned_data.get('content')
			category_id = form.cleaned_data.get('category') # 获取分类id,因为是通过外键获取的id,需要通过NewCategory来获取实际分类名称
			category = NewCategory.objects.get(pk=category_id) # 获取分类名
			News.objects.create(title=title,desc=desc,thumbnail=thumbnail,content=content,category=category,author=request.user)
			return restful.ok()
		else:
			return restful.params_error(message=form.get_error())
		return redirect(reverse('news_list'))
'''
	# dispatch函数解释,当把装饰器命名未dispatch方法时，它就会对请求进行判断，如果时get请求，就调用get函数；如果请求时post请求时，
	就调用post请求。这样装饰器就可以把两种请求都涉及到
	def dispatch(self, request, *args, **kwargs):
		if request.method == 'GET':
			return self.get(request)
		elif request.method == 'POST':
			return self.post(request)

'''


'''定义一个编辑新闻的视图函数'''
#加入装饰器验证是否登录，登录执行该函数，未登录直接跳转到对应的url中
@method_decorator([login_required(login_url='/account/login/'),xfz_permission_required(News)],name='dispatch')
class EditNewsViem(View):
	def get(self,request):
		pk = request.GET.get('pk')
		news = News.objects.get(pk=pk)
		categories = NewCategory.objects.all()
		context = {
			'news':news,
			'categories':categories
		}
		return render(request,'cms/write_news.html',context=context)
	def post(self,request):
		form = EditNewsForm(request.POST)
		if form.is_valid():
			pk = form.cleaned_data.get('pk')
			title = form.cleaned_data.get('title')
			desc = form.cleaned_data.get('desc')
			category_id = form.cleaned_data.get('category')
			thumbnail = form.cleaned_data.get('thumbnail')
			content = form.cleaned_data.get('content')
			category = NewCategory.objects.get(pk=category_id)
			News.objects.filter(pk=pk).update(
				title = title,
				desc = desc,
				thumbnail=thumbnail,
				content=content,
				category=category
			)
			return restful.ok()
		else:
			return restful.params_error(form.get_error())


'''定义一个删除新闻的视图函数'''
@xfz_permission_required(News)
def delete_news(request):
	pk = request.POST.get('pk')
	News.objects.filter(pk=pk).delete()
	return restful.ok()



'''
# 定义一个分类函数，返回一个分类函数的模板，返回一个分类页界面
'''
@method_decorator([login_required(login_url='/account/login/'),xfz_permission_required(NewCategory)],name='dispatch')
# @xfz_permission_required(NewCategory) ### 对于使用class定义的函数，装饰器的使用需要注意，不能使用这种方式，这种只适合def直接定义的函数
class NewsCategoryViem(View):
	def get(self,request):
		# categories是指所有的类别,使用id进行排序
		categories = NewCategory.objects.order_by ('-id') # 获得所有的分类集合，排序按照'-id'的顺序
		'''使用select_related方法获取对象，在对该对象进行处理时，不用经过数据库查询了，减少了查询次数'''
		newses = News.objects.select_related('category') # 从新闻表中按照分类筛选出一个集合
		category_nums = {} # 定义一个空字典，用于后面存放，分类及对应的分类数量

		# 通过一个循环得到分类名及对应分类新闻的数量，并将两者以键值对的形式存在字典category_nums中
		for category in categories:
			'''获取各分类数量'''
			# 方法1：使用len()方法获取长度：
			# 通过分类名对newses数据进行过滤，用len()获取该分类新闻的数量
			nums = len(newses.filter(category__name=category.name))
			# 方法2：使用count()方法统计数量：
			# nums = newses.filter(category__name=category.name).count()
			# 将筛选得到的每一个分类及分类数量以键值对的形式存在字典中
			# 其中将category作为字典键传入html文件是为了后面js文件编辑分类名时取category.id
			category_nums[category] = nums
			print (type (category_nums), "category:%s" % category, "num:%s" % nums, "category_nums%s"%category_nums)

		context = {
			'categories': categories,
			'category_nums':category_nums
		}
		return render (request, 'cms/news_category.html', context=context)


'''
# 定义一个添加分类的视图函数，对添加信息进行判断，不存在就添加，存在就返回‘已经存在信息
'''
# 限制这个视图函数只能通过post请求才能够进行访问
@require_POST
@xfz_permission_required(NewCategory)
def add_news_category(request):
	name = request.POST.get('name')
	# 对名称做一个确认，使用以下定义，如果存在会返回一个Ture，否则返回一个Flase
	exists = NewCategory.objects.filter(name=name).exists()
	if not exists:
		NewCategory.objects.create(name=name)
		return restful.ok()
	else:
		return restful.params_error(message='该分类已经存在！')

	# 定义编辑的视图函数
@require_POST
@xfz_permission_required(NewCategory)
def edit_news_category(request):
	form = EditNewsCategoryForm(request.POST)
	if form.is_valid():
		pk = form.cleaned_data.get('pk')
		name = form.cleaned_data.get('name')
		try:
			NewCategory.objects.filter(pk=pk).update(name=name)
			return restful.ok()
		except:
			return restful.params_error(message='这个分类不存在！')
	else:
		return restful.params_error(message=form.get_error())

'''
# 定义一个删除分类的视图函数
'''
@require_POST
@xfz_permission_required(NewCategory)
def delete_news_category(request):
	pk = request.POST.get('pk')
	try:
		NewCategory.objects.filter(pk=pk).delete()
		return restful.ok()
	except:
		return restful.params_error(message='该分类不存在！')

from django.core.files.uploadedfile import InMemoryUploadedFile


'''轮播图相关函数定义'''
'''#1 展示轮播图界面的视图函数'''
@xfz_permission_required(Banner)
def banners(request):
	return render(request,'cms/banners.html')

'''#2 定义一个将数据库存入的所有数据显示在banner页面'''
@xfz_permission_required(Banner)
def banner_list(request):
	# 获取数据库所有数据，然后序列化，或者直接获取数据
	# 获取Banner模型中所有数据
	# values:返回的还是QuerySet,只不过在QuerySet中，存在的不是模型，而是字典
	banners = list(Banner.objects.all().values()) # 直接将获取数据转换为列表
	return restful.result (data={"banners": banners})
''' 测试用语句：
	for banner in banners:
		print(banner['id']) # 测试输出数据库数据的id
	return restful.ok()
'''


'''#3 添加轮播图函数'''
@xfz_permission_required(Banner)
def add_banner(request):
	form = AddBanner(request.POST) # 表单赋值
	if form.is_valid(): # 如果表单验证成功
		# 获取表单那中的参数
		image_url = form.cleaned_data.get('image_url')
		link_to = form.cleaned_data.get('link_to')
		priority = form.cleaned_data.get('priority')
		# 将表单中获取的参数写入数据库创建的对应的表单中
		banner = Banner.objects. create(image_url=image_url,link_to=link_to,priority=priority)
		return restful.result(data={'banner_id':banner.pk}) # 返回轮播图的id
	else:
		return restful.params_error(message=form.get_error()) #网页弹出函数get_error()返回的错误

'''删除轮播图函数'''
@xfz_permission_required(Banner)
def delete_banner(request):
	banner_id = request.POST.get('banner_id') # 获取要删除的轮播图id
	Banner.objects.filter(pk=banner_id).delete() # 按id查找数据，并删除
	return restful.ok()


'''编辑轮播图数据'''
@xfz_permission_required(Banner)
def edit_banner(request):
	form = EditBannerForm(request.POST)
	if form.is_valid():
		pk = form.cleaned_data.get('pk')
		image_url = form.cleaned_data.get ('image_url')
		link_to = form.cleaned_data.get ('link_to')
		priority = form.cleaned_data.get ('priority')
		# 将表单中获取的参数写入数据库创建的对应的表单中
		banner = Banner.objects.filter(pk=pk).update(image_url=image_url, link_to=link_to, priority=priority) # 数据库查找并更新
		return restful.ok()
	else:
		return restful.params_error(message=form.get_error())


'''
# 定义一个文件传输视图函数
'''
@require_POST
@staff_member_required(login_url='/') #?
def upload_file(request):
	# 定义一个变量用来获取上传文件
	# file变量就是 'InMemoryUploadedFile'类型的函数
	file = request.FILES.get('upfile')
	if not file:
		return restful.params_error(message='没有上传任何文件！')
	name = file.name
	filepath = os.path.join(settings.MEDIA_ROOT,name)
	with open(filepath,'wb')as fp: # 以数据流的形式进行存储
		for chunk in file.chunks():
			fp.write(chunk) # chunk使用一种遍历的形式，以定义的一定量，对文件进行传输，保证内存不被溢出
		# 最终返回一个文件路径+文件名
		# / media / 代码框架.png
		# http://127.0.0.1:9000/media/代码框架.png
		#不讲url写死，自动获取url 其中request.build_absolute_uri()可以获取前面的所有链接，我们只需要将"settings.MEDIA_URL+name"后面的路径加入即可组成一个完整的url
		url = request.build_absolute_uri(settings.MEDIA_URL+name)
		return restful.result(data={"url":url})

'''
定义一个七牛云文件传输的函数
'''
@require_GET
@staff_member_required(login_url='/') #?
def qntoken(request):
	# 七牛云中给出的访问和私有密钥
	access_key = 'AnE70UQaiqokVXUT7v3BGYNAVWo5oey8UA3fEdsD'
	secretkey = 'BIGPCz55HcnTtq3RqDgMfeLUtvwTaBGnVKNs4gyN'

	q = qiniu.Auth(access_key,secretkey)

	bucket = 'achjiangspace' # 可修改，七牛云中创建的存储空间

	token = q.upload_token(bucket)

	return restful.result(data={'token':token})