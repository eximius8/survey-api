from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

import surveys.views as survey_views

router = DefaultRouter()

router.register(r'surveys', survey_views.PollViewSet)
router.register(r'questions', survey_views.QuestionViewSet) 
router.register(r'answers', survey_views.AnswerViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('rest_registration.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls))
]
