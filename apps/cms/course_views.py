from django.views.generic import View # 使用类方法定义视图函数引入的View模块
from django.shortcuts import render
from apps.course.models import CourseCategory,Teacher,Course
from .forms import AddCourseForm # 导入需要的form表单
from utils import restful # 导入返回信息判断文件

'''定义一个发布课程的视图函数'''
class PubCourse(View):
	def  get(self,request):
		context = {
			'categories':CourseCategory.objects.all(),
			'teachers':Teacher.objects.all()
		}
		return render(request,'cms/pub_course.html',context=context)

	def post(self,request):
		form = AddCourseForm(request.POST)
		if form.is_valid():
			# 从form表单中获取数据赋值给model中定义的变量
			title = form.cleaned_data.get('title')
			category_id = form.cleaned_data.get('category_id')
			teacher_id = form.cleaned_data.get('teacher_id')
			video_url = form.cleaned_data.get('video_url')
			cover_url = form.cleaned_data.get('cover_url')
			price = form.cleaned_data.get('price')
			duration = form.cleaned_data.get('duration')
			profile = form.cleaned_data.get('profile')
			# 从form表单中获取的id数据,通过对应模型获取到category和teacher的具体值
			category = CourseCategory.objects.get(pk=category_id)
			teacher = Teacher.objects.get(pk=teacher_id)

			# 将以上整理的数据写入数据库的Course模型
			Course.objects.create(
				title=title,
				category = category,
				teacher = teacher,
				video_url = video_url,
				cover_url = cover_url,
				price = price,
				duration = duration,
				profile = profile
			)

			return restful.ok()
		else:
			return restful.params_error(form.get_error())
