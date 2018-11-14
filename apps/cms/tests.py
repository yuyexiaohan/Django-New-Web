from django.test import TestCase, Client, RequestFactory
from apps.news.models import News, NewCategory
from apps.xfzauth.models import User


class NewsTest(TestCase):
	"""新闻列表测试"""
	def setUp(self):
		self.client = Client()
		self.factory = RequestFactory()

	def test_news(self):
		pass

