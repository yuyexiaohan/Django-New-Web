from django.urls import path
from . import views

app_name = 'payinfo'

urlpatterns = [
	path('',views.index,name='index'),
	path('payinfo_order',views.payinfo_order,name='payinfo_order'),
	path('notify_view/',views.notify_view,name='notify_view'),
	path('download_payinfo/',views.download_payinfo,name='download_payinfo'),
]