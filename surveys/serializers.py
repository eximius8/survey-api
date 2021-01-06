from rest_framework import serializers

from .models import Poll, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):

	id = serializers.IntegerField(required=False)

	class Meta:
		model = Answer
		fields = ['id', 'option',]
		#read_only_fields = ['id',]



class QuestionSerializer(serializers.ModelSerializer):

	answers = AnswerSerializer(many=True, required=False)

	
	def create(self, validated_data):

		if validated_data['questiontype'] == 'T' and 'answers' in validated_data:
			# если ответ в виде текста, а пользователь предоставил варианты ответов
			raise serializers.ValidationError("Для текстового ответа указывать варианты ответа не нужно")

		question = Question.objects.create(questiontype=validated_data['questiontype'],
			questiontext=validated_data['questiontext'],
			poll=validated_data['poll'],)		
			
		answers = validated_data.pop('answers')		
		
		for answer in answers:
			Answer.objects.create(question=question, **answer)
		return question

	def update(self, instance, validated_data):

		if validated_data['questiontype'] == 'T' and 'answers' in validated_data:			
			raise serializers.ValidationError("Для текстового ответа указывать варианты ответа не нужно")

		# update question instance
		instance.questiontype = validated_data.get('questiontype', instance.questiontype)
		instance.questiontext = validated_data.get('questiontext', instance.questiontext)
		instance.save()

		# answers submitted 
		submited_answers = validated_data.get('answers')
		submitted_answer_ids = []	
		
		# updating bound answers
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
				Answer.objects.create(question=instance, **answer)

		for answer in instance.answers.all():
			if not answer.pk in submitted_answer_ids:
				answer.delete()		

		return instance


	class Meta:
		model = Question
		fields = ['id', 'questiontext', 'questiontype', 'poll', 'answers']
		read_only_fields = ['id',]


class PollDetailSerializer(serializers.ModelSerializer):

	questions = QuestionSerializer(many=True, required=False)

	class Meta:
		model = Poll
		fields = ['id', 'name', 'start_date', 'end_date', 'questions']
		read_only_fields = ['id',]


