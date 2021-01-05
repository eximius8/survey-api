from django.db import models



class Poll(models.Model):

	name = models.CharField(max_length=200, blank=False, null=False, verbose_name="Название опроса")
	description = models.TextField(verbose_name="Описание опроса", blank=True, null=True)
	start_date = models.DateField(auto_now=True, auto_now_add=False, editable=False)
	end_date = models.DateField(editable=True)

	def __str__(self):
		return self.name


class Question(models.Model):

	poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
	questiontype = models.CharField(max_length=200, blank=False, null=False, verbose_name="Название опроса")


class Answer(models.Model):

	question = models.ForeignKey(Question, on_delete=models.CASCADE)


