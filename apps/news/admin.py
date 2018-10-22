from django.contrib import admin
from . import models


class NewCategoryAdmin(admin.ModelAdmin):
	"""NewCategory的列展示"""
	list_display = ('id', 'name',)
	list_filter = ('name',)
	search_fields = ('username',)
	list_per_page = 2


class NewsAdmin(admin.ModelAdmin):
	"""News的列展示"""
	list_display = ('id', 'title', 'thumbnail', 'pub_time', 'author',)
	list_filter = ('title', 'author')
	search_fields = ('title', 'author')
	list_per_page = 2


class BannerAdmin(admin.ModelAdmin):
	"""NBanner的列展示"""
	list_display = ('id', 'image_url', 'priority', 'link_to', 'pub_time')
	list_filter = ('priority',)
	search_fields = ('priority',)
	list_per_page = 2


class CommentAdmin(admin.ModelAdmin):
	"""Comment的列展示"""
	list_display = ('id', 'content', 'pub_time', 'news', 'author',)
	list_filter = ('news', 'author',)
	search_fields = ('content', 'news', 'author',)
	list_per_page = 2


admin.site.register(models.NewCategory, NewCategoryAdmin)
admin.site.register(models.News, NewsAdmin)
admin.site.register(models.Banner, BannerAdmin)
admin.site.register(models.Comment, CommentAdmin)
