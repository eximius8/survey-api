from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import redirect
from django.urls import reverse, path

from wagtail.api.v2.router import WagtailAPIRouter

from surveys.endpoints import SurveyAPIEndpoint


api_router = WagtailAPIRouter('wagtailapi')

api_router.register_endpoint('surveys', SurveyAPIEndpoint)
