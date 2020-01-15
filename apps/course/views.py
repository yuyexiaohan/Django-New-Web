import time
import os
import hmac
import hashlib
from hashlib import md5  # 导入md5加密

from django.conf import settings
from django.shortcuts import render
from django.shortcuts import reverse  # 重定向模块
from django.views.decorators.csrf import csrf_exempt  # 导入装饰器
from django.shortcuts import redirect
from apps.xfzauth.decorators import xfz_permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required  # 导入登录验证函数
from django.utils.decorators import method_decorator  # 验证登录才能访问函数的装饰器

from utils import restful
from .models import Course, CourseOrder  # 导入课程模板


# method_decorator是一个将装饰器函数，转换为装饰器方法的
# @method_decorator(xfz_permission_required(Course),name='dispatch')
# @xfz_permission_required
def course_index(request):
    """课程资讯"""
    context = {
        'courses': Course.objects.all()  # 获取所有课程信息
    }
    return render(request, 'course/course_index.html', context=context)


# @method_decorator(login_required(login_url='/account/login/'))
@login_required(login_url='/account/login/')
def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    # if request.user.is_authenticated():
    # 	buyed = CourseOrder.objects.filter(buyer=request.user,course=course,status=2)
    # else:
    # 	buyed = True
    buyed = CourseOrder.objects.filter(
        buyer=request.user, course=course, status=2).exists()
    context = {
        'course': course,
        'buyed': buyed
    }
    return render(request, 'course/course_detail.html', context=context)


def course_token(request):
    video_url = request.GET.get('video_url')
    course_id = request.GET.get('course_id')

    # 判断课程是否免费，免费直接获取token值，付费则进行订单支付后获取token值
    course_price = Course.objects.get(pk=course_id).price
    if course_price != 0:
        buyed = CourseOrder.objects.filter(
            course_id=course_id, buyer=request.user, status=2).exists()
        if not buyed:
            return restful.params_error(message='请先购买课程！')

    expiration_time = int(time.time()) + 2 * 60 * 60

    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    # file=http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.m3u8
    extension = os.path.splitext(video_url)[1]
    media_id = video_url.split('/')[-1].replace(extension, '')

    # unicode->bytes=unicode.encode('utf-8')bytes
    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
    print("course_token:", token)
    return restful.result(data={'token': token})


def course_order(request):
    """课程支付"""
    course_id = request.GET.get('course_id')
    course = Course.objects.get(pk=course_id)
    buyed = CourseOrder.objects.filter(
        buyer=request.user, course=course, status=2).exists()
    if buyed:
        return redirect(
            reverse(
                "course:course_detail",
                kwargs={
                    'course_id': course.pk}))
    order = CourseOrder.objects.create(
        amount=course.price,
        course=course,
        buyer=request.user,
        status=1)
    context = {
        'course': course,
        # .build_absolute_uri()是一个构建绝对路径或相对路径的url
        'notify_url': request.build_absolute_uri(reverse("course:notify_url")),
        'order': order,
        'return_url': request.build_absolute_uri(reverse('course:course_detail', kwargs={'course_id': course.pk}))
    }

    return render(request, 'course/create_order.html', context=context)


def order_key(request):
    """支付加密"""
    goodsname = request.POST.get('goodsname')
    istype = request.POST.get('istype')
    notify_url = request.POST.get('notify_url')
    orderid = request.POST.get('orderid')
    price = request.POST.get('price')
    return_url = request.POST.get('return_url')

    token = settings.PAY_TOKEN
    uid = settings.PAY_UID
    orderuid = str(request.user.pk)

    key = md5(
        (goodsname +
         istype +
         notify_url +
         orderid +
         orderuid +
         price +
         return_url +
         token +
         uid).encode("utf-8")).hexdigest()
    # key = md5 ("".join ([goodsname, istype, notify_url, orderuid, orderuid, price, return_url, token, uid])
    # .encode ("utf-8")).hexdigest ()
    return restful.result(data={'key': key})


@csrf_exempt
def notify_view(request):
    """第三方支付paysAPI要求返回的回调"""
    orderid = request.POST.get('orderid')
    CourseOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()
