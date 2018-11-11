from django.test import TestCase, Client, RequestFactory


class NewsTest(TestCase):
	"""新闻列表测试"""
	def setUp(self):
		self.client = Client()
		self.factory = RequestFactory()

	def test_news(self):
		pass

