from wagtail.api.v2.views import BaseAPIViewSet
from .models import Survey

class SurveyAPIEndpoint(BaseAPIViewSet):

    model = Survey

    body_fields = BaseAPIViewSet.body_fields + [
        'name',
        'description',
        'date_from',
        'date_to',
        'questions',
    ]

    listing_default_fields = BaseAPIViewSet.listing_default_fields = [
        'name',        
        'date_from',
        'date_to',
    ]