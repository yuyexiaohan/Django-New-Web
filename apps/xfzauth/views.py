from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import LoginFrom, RegisterForm  # 导入form表单
# authentivate 用来验证用户是否登录，login和logout的登录和登出
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # 导入messages模块进行错误消息的传递
from utils.captcha.hycaptcha import Captcha
from io import BytesIO  # 用来存储这些字节流
from django.http import HttpResponse
from utils.aliyunsdk import aliyun
from .models import User
# from django.forms.utils import ErrorDict
from utils import restful

# 两种写法
# 1.定义函数法
# def login_view(request):
# 	if request.method == 'GET':
# 		return render(request,'auth/login.html')


class LoginView(View):
    """登录  2.使用类写法"""

    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        form = LoginFrom(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get("telephone")
            password = form.cleaned_data.get("password")
            remember = form.cleaned_data.get("remember")
            # authenticate函数是判断凭证是否有效，有效返回一个user对象
            user = authenticate(request, username=telephone, password=password)
            if user:
                login(request, user)  # 登陆成功
                if remember:
                    # 如果设置过期时间位None,那么就会使用默认的过期时间
                    # 默认的过期时间位2个星期，14天
                    print("session默认时长14天")
                    request.session.set_expiry(None)
                else:
                    # 如果设置过期时间位0，那么浏览器关闭时就会结束
                    print("session时长为关闭浏览器时结束")
                    request.session.set_expiry(0)
                # 如果登陆成功，就返回首页
                print("验证登录成功！")
                return redirect(reverse('news:index'))
            else:
                # print("用户名或密码错误！", '电话 ：%s' % telephone, '密码 ：%s' % password)
                messages.info(request, "用户名或密码错误！")
                # message中包含由3中消息，1.info：提示消息；2.error：错误消息；3.debug：调试消息
                return redirect(reverse('xfzauth:login'))
        else:
            # print("表单验证失败！")
            messages.info(request, "表单验证失败！")
            return redirect(reverse('xfzauth:login'))

# 1 Form表单版本的注册代码
# class RegisterView(View):
# 	def get(self,request):
# 		return render(request,"auth/register.html") # render 是重定向，将链接跳转到指定的url;
#
# 	def post(self,request):
# 		form = RegisterForm(request.POST)
# 		if form.is_valid() and form.validate_data(request):
# 			telephone = form.cleaned_data.get('telephone')
# 			username = form.cleaned_data.get('username')
# 			password = form.cleaned_data.get('password')
# 			user = User.objects.create_user(telephone=telephone,username=username,password=password)
# 			# 这是一个django自带的登录函数
# 			login(request,user)
# 			return redirect(reverse('news:index'))
# 		else:
# 			message = form.get_error()
# 			messages.info(request,message)
# 			return redirect(reverse('xfzauth:register'))


class RegisterView(View):
    """注册"""

    def get(self, request):
        return render(request, "auth/register.html")
    # render 是重定向，将链接跳转到指定的url;

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid() and form.validate_data(request):
            telephone = form.cleaned_data.get('telephone')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(
                telephone=telephone, username=username, password=password)
            print('电话：%s' % telephone, '密码：%s' % password)
            login(request, user)  # 注册成功后，直接跳转到登录状态
            return restful.ok()
        else:
            message = form.get_error()
            return restful.params_error(message=message)


def logout_view(request):
    """退出登录"""
    logout(request)
    return redirect('/')


def img_captcha(request):
    """图形验证码"""
    text, image = Captcha.gene_code()
    # image不是一个HttpResponse可识别对象
    # 因此先要将image变成一个数据流才能放到HttpResponse上
    # ByteIO:相当于一个管道，用来存储二进制字节流的
    out = BytesIO()
    image.save(out, 'png')
    # 文件指针设置为0的位置，按照存储，从0开始
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()
    request.session['img_captcha'] = text
    return response


def sms_capacha(request):
    """短信验证码"""
    code = Captcha.gene_text()
    print('code:', code)
    # 获取方式是/account/sms_captcha/?telephone=12345678900
    telephone = request.GET.get('telephone')
    result = aliyun.send_sms(telephone, code=code)  # 前端会用到该参数
    print(telephone, code)
    request.session['sms_captcha'] = code
    return HttpResponse('success')
