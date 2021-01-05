from rest_framework import serializers

from .models import Poll, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Answer
		fields = ['option',]


class QuestionSerializer(serializers.ModelSerializer):

	answers = AnswerSerializer(many=True)

	class Meta:
		model = Question
		fields = ['questiontext', 'questiontype', 'answers']


class PollSerializer(serializers.ModelSerializer):

	questions = QuestionSerializer(many=True)

	class Meta:
		model = Poll
		fields = ['name', 'description', 'start_date', 'end_date', 'questions']