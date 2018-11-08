"""自定义一个登录验证装饰器"""

from utils import restful  # 导入错误信息提示文件
from django.shortcuts import redirect  # 导入重定向函数
from functools import wraps
from django.contrib.auth.models import Permission, ContentType
from django.http import Http404


def xfz_login_required(func):
    """判断用户是否登陆"""
    def wapper(request, *args, **kwargs):
        # 判断用户是否登录
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='请先登录！')  # 返回一个unauth的401错误
            else:
                return redirect('/')
    return wapper
# 返回一个文件名，这样就可以写成一个装饰器


"""
def xfz_permission_required(model):

	def decorator(viewfunc):
		@wraps(viewfunc)
		def _wrapper(request,*args,**kwargs):
			content_type = ContentType.objects.get_for_model(model)
			permissions = Permission.objects.filter(content_type=content_type)

			codenames = [content_type.app_label+"."+permissions.codename for permission in permissions]

			# has_perms：只能采用字符串的形式判断
			# 字符串的形式为：app_label.codename
			result = request.user.has_perms(codenames)
			if result:
				return viewfunc(request,*args,**kwargs)
			else:
				raise Http404()
		return _wrapper
	return decorator

def xfz_superuser_required(viewfunc):

	@wraps(viewfunc)
	def _wrapper(request,*args,**kwargs):
		if request.user.is_superuser:
			return viewfunc(request,*args,**kwargs)
		else:
			raise Http404()
	return _wrapper
"""

"""t代码"""


def xfz_permission_required(model):
    def decorator(viewfunc):
        @wraps(viewfunc)
        def _wrapper(request, *args, **kwargs):
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)

            codenames = [content_type.app_label + "." +
                         permission.codename for permission in permissions]

            # has_perms：只能采用字符串的形式判断
            # 字符串的形式为：app_label.codename
            result = request.user.has_perms(codenames)
            if result:
                return viewfunc(request, *args, **kwargs)
            else:
                print('=' * 20)
                raise Http404()
        return _wrapper
    return decorator


def xfz_superuser_required(viewfunc):
    @wraps(viewfunc)
    def _wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return viewfunc(request, *args, **kwargs)
        else:
            raise Http404()
    return _wrapper
