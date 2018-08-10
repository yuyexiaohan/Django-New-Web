from django.urls import path
from . import views

app_name = 'xfzauth'

urlpatterns = [
	# path("login/",views.login_view,name='login'), # 第1种写法的url
	path("login/",views.LoginView.as_view(),name='login') ,# 第2种写法的url .as_view()函数是将类转变成函数才能使用
	path("register/",views.RegisterView.as_view(),name='register'),
	path("img_captcha/",views.img_captcha,name='img_captcha'),
	path("sms_captcha/",views.sms_capacha,name='sms_captcha'),
	path("logout/",views.logout_view,name='logout'),
]