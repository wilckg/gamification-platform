"""
URL configuration for backend project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import (
    AdminCreateView,  # Note que mudamos de AdminRegisterView para AdminCreateView
    AlunoCreateView,  # Note que mudamos de AlunoRegisterView para AlunoCreateView
    AdminTokenObtainPairView,
    AlunoTokenObtainPairView,
    PasswordResetRequestView,
    PasswordResetConfirmView
)
from django.views.generic.base import RedirectView

urlpatterns = [
    # Redirecionamento padrão para o admin
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
    
    # Interface de administração do Django
    path("admin/", admin.site.urls),
    
    # API Principal
    path('api/', include([
        # Endpoints de Autenticação
        path('auth/', include([
            # Login para administradores (usando username)
            path('admin/login/', AdminTokenObtainPairView.as_view(), name='admin-login'),
            
            # Login para alunos (usando email)
            path('aluno/login/', AlunoTokenObtainPairView.as_view(), name='aluno-login'),
            
            # Refresh token
            path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
            
            # Registro/Criação de usuários
            path('admin/create/', AdminCreateView.as_view(), name='admin-create'),
            path('aluno/create/', AlunoCreateView.as_view(), name='aluno-create'),
            
            # Recuperação de senha
            path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
            path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
        ])),
        
        # App de Challenges
        path('challenges/', include('challenges.urls')),
    ])),
]