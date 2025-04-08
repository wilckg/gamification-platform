# backend/core/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from challenges.views import ChallengeViewSet, UserChallengeViewSet, RankingViewSet

router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet)
router.register(r'user-challenges', UserChallengeViewSet, basename='userchallenge')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/ranking/', RankingViewSet.as_view({'get': 'list'}), name='ranking'),
    path('api/auth/', include('rest_framework.urls')),
]