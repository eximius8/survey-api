from django.db import models
from django.conf import settings



class Poll(models.Model):

	name = models.CharField(max_length=200, blank=False, null=False, verbose_name="Название опроса")
	description = models.TextField(verbose_name="Описание опроса", blank=True, null=True)
	start_date = models.DateField(auto_now=True, editable=False)
	end_date = models.DateField(editable=True, blank=True, null=True, verbose_name="Дата окончания")

	def __str__(self):
		return self.name


class Question(models.Model):

	QUESTION_TYPES = (('T', 'ответ текстом'),
			          ('S', 'ответ с выбором одного варианта'),
			          ('M', 'ответ с выбором нескольких вариантов'))

	poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')	
	questiontext = models.CharField(max_length=300, blank=False, null=False, 
		verbose_name="Текст вопроса")
	questiontype = models.CharField(max_length=3, choices=QUESTION_TYPES, blank=False, null=False, 
		verbose_name="Название опроса")


class Answer(models.Model):

	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
	option = models.CharField(max_length=200, blank=False, null=False, verbose_name="Вариант ответа")


class UserResponse(models.Model):

	answer = models.OneToOneField(Answer, blank=True, null=True, on_delete=models.CASCADE)
	textresponse = models.TextField(verbose_name="Ответ в виде текста", blank=True, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)