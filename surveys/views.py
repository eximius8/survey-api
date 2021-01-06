from rest_framework import viewsets

from .models import Poll, Question, Answer, UserResponse
from .serializers import PollDetailSerializer, QuestionSerializer, AnswerSerializer



class PollViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Poll.objects.all()
    serializer_class = PollDetailSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]


class QuestionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]