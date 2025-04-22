# challenges/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TrackViewSet,
    ChallengeViewSet,
    UserChallengeViewSet,
    UserTrackProgressViewSet
)

router = DefaultRouter()
router.register(r'tracks', TrackViewSet, basename='track')
router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'user-challenges', UserChallengeViewSet, basename='user-challenge')
router.register(r'user-progress', UserTrackProgressViewSet, basename='user-progress')

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints adicionais
    path('user-progress/current/', 
        UserTrackProgressViewSet.as_view({'get': 'current_progress'}),
        name='user-progress-current'),
]