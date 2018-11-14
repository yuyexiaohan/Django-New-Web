from django.test import TestCase, Client, RequestFactory
from apps.news.models import News, NewCategory
from apps.xfzauth.models import User


class NewsTest(TestCase):
	"""新闻列表测试"""
	def setUp(self):
		self.client = Client()
		self.factory = RequestFactory()
		print ("setUp: Run once for every test method to setup clean data.")

	def test_news_edit(self):
		pass

	def test_news_update(self):
		pass
