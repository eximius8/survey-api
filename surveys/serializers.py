from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Poll, Question, Answer, UserResponse

class UserResponseSerializer(serializers.ModelSerializer):
	"""
	Сериалайзер для ответов пользователей
	"""

	id = serializers.IntegerField(required=False)

	def validate(self, attrs):

		quest = attrs['question']
		if quest.questiontype == "T" and len(attrs['answers']) > 0:
			raise serializers.ValidationError("Для текстового ответа указывать варианты ответа не нужно")
		if quest.questiontype == "S" and len(attrs['answers']) != 1:
			raise serializers.ValidationError("Необходимо выбрать один вариант ответа")
		if quest.questiontype in ["S", "M"] and len(attrs['textresponse']) > 0:
			raise serializers.ValidationError("Для вопроса нужно выбрать вариант(ы) ответа а не текст")
		
		return attrs


	class Meta:
		model = UserResponse
		fields = ['id', 'question', 'answers', 'textresponse', 'userid']
		validators = [
            UniqueTogetherValidator(
                queryset=UserResponse.objects.all(),
                fields=['question', 'userid']
            )
        ]



class AnswerSerializer(serializers.ModelSerializer):
	"""
	Сериалайзер для возможных ответов на вопросы
	"""

	id = serializers.IntegerField(required=False)

	class Meta:
		model = Answer
		fields = ['id', 'option',]		



class QuestionSerializer(serializers.ModelSerializer):
	"""
	Сериалайзер для изменения вопросов
	"""

	answers = AnswerSerializer(many=True, required=False)

	
	def create(self, validated_data):

		answers = validated_data.get('answers', [])

		if validated_data['questiontype'] == 'T' and len(answers) > 0:
			# если ответ в виде текста, а администратор предоставил варианты ответов
			raise serializers.ValidationError("Для текстового ответа указывать варианты ответа не нужно")

		question = Question.objects.create(questiontype=validated_data['questiontype'],
											questiontext=validated_data['questiontext'],
											poll=validated_data['poll'],)
		
		for answer in answers:
			Answer.objects.create(question=question, **answer)
		return question

	def update(self, instance, validated_data):

		# answers submitted 
		submited_answers = validated_data.get('answers', [])
		if validated_data['questiontype'] == 'T' and len(submited_answers) > 0:	
			raise serializers.ValidationError("Для текстового ответа указывать варианты ответа не нужно")

		# update question instance
		instance.questiontype = validated_data.get('questiontype', instance.questiontype)
		instance.questiontext = validated_data.get('questiontext', instance.questiontext)
		instance.save()		
		
		submitted_answer_ids = []	
		
		# updating answers
		for answer in submited_answers:
			answer_id = answer.get('id', None)
			submitted_answer_ids += [answer_id,]
			if answer_id:
				answer_query = Answer.objects.filter(pk=answer_id, question=instance)
				if not answer_query.exists():
					raise serializers.ValidationError(f"Ответ с ID {answer_id} не привязан к данному вопросу")
				answer_instance = answer_query[0]
				answer_instance.option = answer.get('option', answer_instance.option)
				answer_instance.save()
			else:
				new_answer = Answer.objects.create(question=instance, **answer)
				submitted_answer_ids += [new_answer.pk,]
		
		for answer in instance.answers.all():
			if not answer.pk in submitted_answer_ids:
				answer.delete()		

		return instance


	class Meta:
		model = Question
		fields = ['id', 'questiontext', 'questiontype', 'answers', 'poll']
		read_only_fields = ['id']
		

class QuestionInternalSerializer(serializers.ModelSerializer):
	"""
	Сериалайзер для получения списка вопросов
	"""

	id = serializers.IntegerField(required=False)
	answers = AnswerSerializer(many=True, required=False)

	class Meta:
		model = Question
		fields = ['id', 'questiontext', 'questiontype', 'answers']


class PollDetailSerializer(serializers.ModelSerializer):
	"""
	Сериалайзер для опросов
	"""	

	questions = QuestionInternalSerializer(many=True, required=False)


	def create(self, validated_data):

		poll = Poll.objects.create(name=validated_data['name'],
									description=validated_data['description'],
									end_date=validated_data['end_date'],)		
			
		questions = validated_data.get('questions', [])		
		
		for question in questions:
			answers = question.get('answers', [])

			if question['questiontype'] == 'T' and len(answers) > 0:
				# если ответ в виде текста, а администратор предоставил варианты ответов
				raise serializers.ValidationError("Для текстового ответа указывать варианты ответа не нужно")

			question = Question.objects.create(questiontype=question['questiontype'],
												questiontext=question['questiontext'],
												poll=poll,)
			for answer in answers:
				Answer.objects.create(question=question, **answer)

		return poll

	def update(self, instance, validated_data):

		instance.name = validated_data.get('name', instance.name)
		instance.description = validated_data.get('description', instance.description)
		instance.end_date = validated_data.get('end_date', instance.end_date)
		instance.save()

		return instance


	class Meta:
		model = Poll
		fields = ['id', 'name', 'description', 'start_date', 'end_date', 'questions']
		read_only_fields = ['id',]

