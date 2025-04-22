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

# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import (
    AdminRegisterView,
    AlunoRegisterView,
    AdminTokenObtainPairView,
    AlunoTokenObtainPairView,
    PasswordResetRequestView,
    PasswordResetConfirmView
)
from django.views.generic.base import RedirectView
    
urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
    path("admin/", admin.site.urls),
    
    # API
    path('api/', include([
        # Autenticação
        path('auth/', include([
            path('admin/login/', AdminTokenObtainPairView.as_view(), name='admin-login'),
            path('aluno/login/', AlunoTokenObtainPairView.as_view(), name='aluno-login'),
            path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
            path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),
            path('aluno/register/', AlunoRegisterView.as_view(), name='aluno-register'),
            path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
            path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
        ])),
        
        # Challenges App
        path('challenges/', include('challenges.urls')),
    ])),
]

