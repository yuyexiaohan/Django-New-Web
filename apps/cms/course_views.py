from django.views.generic import View  # 使用类方法定义视图函数引入的View模块
from django.shortcuts import render
from apps.course.models import CourseCategory, Teacher, Course
from .forms import AddCourseForm, EditCoursesCategoryForm  # 导入需要的form表单
from utils import restful  # 导入返回信息判断文件
import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.xfzauth.decorators import xfz_permission_required
from apps.course.serializers import TeacherSerializers

# restful表格处理
from django.shortcuts import get_object_or_404, redirect
from apps.course.models import Teacher
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response


logger = logging.getLogger("django")  # 初始化logger模块


# @method_decorator(login_required, name='dispatch')
class PubCourse(View):
    """发布课程"""

    def get(self, request):
        context = {
            'categories': CourseCategory.objects.all(),
            'teachers': Teacher.objects.all()
        }
        return render(request, 'cms/pub_course.html', context=context)

    def post(self, request):
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
                category=category,
                teacher=teacher,
                video_url=video_url,
                cover_url=cover_url,
                price=price,
                duration=duration,
                profile=profile
            )
            return restful.ok()
        else:
            return restful.params_error(form.get_error())


# @login_required()
class CourseCategoryViem(View):
    """课程分类"""

    def get(self, request):
        # categories是指所有的类别,使用id进行排序
        categories = CourseCategory.objects.order_by(
            '-id')  # 获得所有的分类集合，排序按照'-id'的顺序
        '''使用select_related方法获取对象，在对该对象进行处理时，不用经过数据库查询了，减少了查询次数'''
        courses = Course.objects.select_related('category')  # 从新闻表中按照分类筛选出一个集合
        category_nums = {}  # 定义一个空字典，用于后面存放，分类及对应的分类数量

        # 通过一个循环得到分类名及对应分类新闻的数量，并将两者以键值对的形式存在字典category_nums中
        for category in categories:
            '''获取各分类数量'''
            # 方法1：使用len()方法获取长度：
            # 通过分类名对newses数据进行过滤，用len()获取该分类新闻的数量
            nums = len(courses.filter(category__name=category.name))
            print("*"*50, categories, "-"*50)
            # 方法2：使用count()方法统计数量：
            # nums = courses.filter(category__name=category.name).count()
            # 将筛选得到的每一个分类及分类数量以键值对的形式存在字典中
            # 其中将category作为字典键传入html文件是为了后面js文件编辑分类名时取category.id
            category_nums[category] = nums
            # print(type(category_nums), "category:%s" %category, "num:%s" %nums, "category_nums%s" %category_nums)

        context = {
            'categories': categories,
            'category_nums': category_nums
        }
        return render(request, 'cms/course_category.html', context=context)


@login_required()
def add_course_category(request):
    """添加课程分类"""
    name = request.POST.get("name")
    exist = CourseCategory.objects.filter(name=name).exists()
    if not exist:
        CourseCategory.objects.create(name=name)
        logger.info('添加文章分类:%s！' % name)
        return restful.ok()
    logger.warning("文章分类:'%s'已经存在！'" % name)
    return restful.params_error(message='该分类已经存在！')


@login_required()
def edit_course_category(request):
    """编辑分类"""
    form = EditCoursesCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            CourseCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except Exception as e:
            logger.error("修改文章分类报错：%s" % e)
            return restful.params_error(message="这个分类不存在！")
    else:
        return restful.params_error(message=form.get_error())


@login_required()
def delete_course_category(request):
    """删除分类"""
    pk = request.POST.get("pk")
    try:
        CourseCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except Exception as e:
        logger.error("删除分类出错：%s" % e)
        return restful.params_error(message="这个分类不存在或已被删除，请刷新界面重新查看！")


# restful API接口规范化
# 方法1：方法的restful

# 方法2：类的restful
# 2-1 使用APIView方法实现
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status


# class CourseTeacherList(APIView):
#     """课程老师信息的增删改"""
#
#     def get(self, request, format=None):
#         """获取老师信息列表"""
#         teacher = Teacher.objects.all()
#         serializer = TeacherSerializers(teacher, many=True)
#         return Response(data=serializer.data)
#
#     def post(self, request, format=None):
#         """提交老师信息"""
#         serializer = TeacherSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
#
#
# class CourseTeacherDetail(APIView):
#     """查找更新一个实例"""
#
#     def get_object(self, pk):
#         try:
#             return Teacher.objects.get(pk=pk)
#         except Teacher.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         """获取"""
#         teacher = self.get_object(pk)
#         serializer = TeacherSerializers(teacher)
#         return Response(serializer.data)
#
#     def put(self, request, pk ,format=None):
#         """更新"""
#         teacher = self.get_object(pk)
#         serializer = TeacherSerializers(teacher, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer)


# 2-2 使用mixins
# from rest_framework import mixins
# from rest_framework import generics
# from apps.course.models import Teacher
# from apps.course.serializers import TeacherSerializers
#
#
# class CourseTeacherList(mixins.CreateModelMixin,
#                         mixins.ListModelMixin,
#                         generics.GenericAPIView):
#     """课程老师信息的增删改"""
#     queryset = Teacher.objects.all()
#     serializer_class = TeacherSerializers
#
#     def get(self, request, *args, **kwargs):
#         """获取老师信息列表"""
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         """提交老师信息"""
#         return self.create(request, *args, **kwargs)
#
#
# class CourseTeacherDetail(mixins.RetrieveModelMixin,
#                           mixins.UpdateModelMixin,
#                           mixins.DestroyModelMixin,
#                           generics.GenericAPIView):
#     """查找更新一个实例"""
#
#     queryset = Teacher.objects.all()
#     serializer_class = TeacherSerializers
#
#     def get(self, request, *args, **kwargs):
#         """获取"""
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         """更新"""
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         """删除"""
#         return self.delete(request, *args, **kwargs)

# 2-3 使用通用的类视图
# from apps.course.models import Teacher
# from apps.course.serializers import TeacherSerializers
# from rest_framework import generics
#
#
# class CourseTeacherList(generics.ListCreateAPIView):
#     """课程老师信息的增删改"""
#     queryset = Teacher.objects.all()
#     serializer_class = TeacherSerializers
#
#
# class CourseTeacherDetail(generics.RetrieveUpdateDestroyAPIView):
#     """查找更新一个实例"""
#     queryset = Teacher.objects.all()
#     serializer_class = TeacherSerializers


class CourseTeacherList(APIView):
    """课程老师信息的增删改"""
    render_classes = [TemplateHTMLRenderer]
    template_name = "cms/course_teacher.html"

    def get(self, request):
        """获取老师信息列表"""
        queryset = Teacher.objects.all()
        return Response({'teachers': queryset})

#     def post(self, request, format=None):
#         """提交老师信息"""
#         serializer = TeacherSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CourseTeacherDetail(APIView):
    """查找更新一个实例"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cms/course_teacher_detail.html"

    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """获取"""
        # teacher = self.get_object(pk)
        teacher = get_object_or_404(Teacher, pk=pk)
        serializer = TeacherSerializers(teacher)
        return Response({"serializer": serializer, "teacher": teacher})

    def post(self, request, pk):
        """创建"""
        # teacher = self.get_object(pk)
        teacher = get_object_or_404(Teacher, pk=pk)
        serializer = TeacherSerializers(teacher, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'teacher': teacher})
        serializer.save()
        return redirect('cms: course_teacher')

    def put(self, request, pk):
        """更新"""
        # teacher = self.get_object(pk)
        teacher = get_object_or_404(Teacher, pk=pk)
        serializer = TeacherSerializers(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer)
