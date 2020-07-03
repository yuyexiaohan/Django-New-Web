"""django_01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static  # 用来拼接一些静态文件路径
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # django自带的admin用户路由界面
    path('', include('apps.news.urls')),  # 新闻路由界面，apps.name用于区分命名空间下对应的urls
    path('account/', include('apps.xfzauth.urls')),  # 登录注册界面的主urls
    path('course/', include('apps.course.urls')),  # 创业课堂页面的主urls
    path('payinfo/', include('apps.payinfo.urls')),  # 支付界面urls
    path('cms/', include('apps.cms.urls')),  # 后台管理系统urls
    path("ueditor/", include("apps.ueditor.urls")),  # 文本编辑器urls
    # 1 将static写在urlpatterns里的写法：
    # static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)[0],
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 2 static写在外面的写法

# 说明;1.告诉当访问media文件时，可以到后面定义的settings.MEDIA_EOOT目录下寻找。这样就可以直接用浏览器通过对应的文件路径访问文件。如果不做这个配置，浏览器是不能直接根据路径访问文件的
# 2.因为urlpatterns是一个列表参数，static()返回值也是一个列表，使用“+”直接变成列表相加，最终的static()也是urlpatterns中的一个元素。等效于：urlpatterns
# += static()

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/",include(debug_toolbar.urls))]

if settings.DEBUG:
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
