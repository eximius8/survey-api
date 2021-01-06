from rest_framework import viewsets, mixins

from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission

from .models import Poll, Question, Answer, UserResponse
from .serializers import PollDetailSerializer, QuestionSerializer, AnswerSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class PollViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Poll.objects.all()
    serializer_class = PollDetailSerializer
    permission_classes = [IsAdminUser|ReadOnly]


class QuestionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser|ReadOnly]

class AnswerViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAdminUser|ReadOnly]