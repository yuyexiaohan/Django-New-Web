from django.test import TestCase, Client


class NewsTest(TestCase):
	"""新闻列表测试"""
	def setUp(self):
		self.client = Client()

	def test_news(self):
		pass

