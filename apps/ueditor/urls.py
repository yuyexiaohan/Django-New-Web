#encoding: utf-8

from django.urls import path
from . import views
from django.conf import settings

app_name = 'ueditor'

urlpatterns = [
    path("upload/",views.UploadView.as_view(),name='upload')
]

if hasattr(settings,"UEDITOR_UPLOAD_PATH"):
    urlpatterns += [
        path("f/<filename>",views.send_file,name='send_file')
    ]
