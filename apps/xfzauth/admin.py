from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
	"""user的列展示"""
	list_display = ('id', 'telephone', 'username', 'email', 'is_active', 'gender', 'date_joined', 'is_staff')
	list_filter = ('gender', 'is_staff', 'is_active')
	search_fields = ('telephone', 'username', 'email')
	list_per_page = 2
	list_select_related = True

admin.site.register(models.User, UserAdmin)
