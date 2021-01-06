from rest_framework import viewsets

from .models import Poll
from .serializers import PollSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]