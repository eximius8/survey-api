from rest_framework import viewsets, mixins

from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission

from .models import Poll, Question, Answer, UserResponse
from .serializers import PollDetailSerializer, QuestionSerializer, AnswerSerializer, UserResponseSerializer


class UserResponseViewSet(viewsets.ModelViewSet):
    """
    Вью для ответов пользователей доступно всем
    """
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer

    filterset_fields = ['userid']
    

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class PollViewSet(viewsets.ModelViewSet):
    """
    Вью для опросов доступно администраторам
    """
    
    queryset = Poll.objects.all()
    serializer_class = PollDetailSerializer
    permission_classes = [IsAdminUser|ReadOnly]
   
    
    filterset_fields ={'end_date': ['gte', 'lte', 'exact', 'gt', 'lt'], }


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Вью для вопросов доступно администраторам
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
    Вью для ответов доступно администраторам
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAdminUser|ReadOnly]