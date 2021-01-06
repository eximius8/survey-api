from rest_framework.test import APIRequestFactory
from django.test import TestCase


class QuestionModelTests(TestCase):	


	factory = APIRequestFactory()
	request = factory.post('/api/answers/', {'title': 'new idea'}, format='json')