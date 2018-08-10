from django.urls import path
from . import views
from . import course_views
from . import staff_views

app_name = 'cms'

urlpatterns = [
	path('',views.index,name='index'),
	path('news_list/',views.NewsList.as_view(),name='news_list'),
	path('write_news/',views.WriteNewsView.as_view(),name='write_news'),
	path('edit_news/',views.EditNewsViem.as_view(),name='edit_news'),
	path('delete_news/',views.delete_news,name='delete_news'),
	path('news_category/',views.NewsCategoryViem.as_view(),name='news_category'),
	path('add_news_category/',views.add_news_category,name='add_news_category'),
	path('edit_news_category/',views.edit_news_category,name='edit_news_category'),
	path('delete_news_category/',views.delete_news_category,name='delete_news_category'),
	path('banners/',views.banners,name='banners'),
	path('banner_list/',views.banner_list,name='banner_list'),
	path('add_banner/',views.add_banner,name='add_banner'),
	path('delete_banner/',views.delete_banner,name='delete_banner'),
	path('edit_banner/',views.edit_banner,name='edit_banner'),
	path('upload_file/',views.upload_file,name='upload_file'),
	path('qntoken/',views.qntoken,name='qntoken'),
]
# 课程相关的url
urlpatterns += [
	path('pub_course/',course_views.PubCourse.as_view(),name = 'pub_course')
]

# 用户管理相关url配置
urlpatterns += [
	path('staffs/',staff_views.staffs,name='staffs'),
	path('add_staff/',staff_views.AddStaffView.as_view(),name='add_staff')
]