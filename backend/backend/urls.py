"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import (
    CustomTokenObtainPairView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    UserRegisterView
)
from django.views.generic.base import RedirectView
    
urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
    path("admin/", admin.site.urls),
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', UserRegisterView.as_view(), name='register'),
    path('api/auth/', include([
        path('login/', TokenObtainPairView.as_view(), name='login'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('register/', UserRegisterView.as_view(), name='register'),
        path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
        path('password-reset-confirm/<uidb64>/<token>/', 
             PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    ])),
]
