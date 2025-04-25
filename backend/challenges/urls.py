from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TrackViewSet,
    ChallengeViewSet,
    UserChallengeViewSet,
    UserTrackProgressViewSet,
    QuestionViewSet,
    OptionViewSet
)

router = DefaultRouter()
router.register(r'tracks', TrackViewSet, basename='track')
router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'user-challenges', UserChallengeViewSet, basename='user-challenge')
router.register(r'user-progress', UserTrackProgressViewSet, basename='user-progress')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'options', OptionViewSet, basename='option')

urlpatterns = [
    path('', include(router.urls)),
    path('user-progress/current/', 
        UserTrackProgressViewSet.as_view({'get': 'current_progress'}),
        name='user-progress-current'),
    path('challenges/<int:challenge_pk>/questions/', 
        QuestionViewSet.as_view({'get': 'list_by_challenge'}), 
        name='challenge-questions'),
    path('questions/<int:question_pk>/options/', 
        OptionViewSet.as_view({'get': 'list_by_question'}), 
        name='question-options'),
]