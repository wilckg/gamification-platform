from django.urls import path
from .views import AlunoProfileView, AvatarUpdateView

urlpatterns = [
    path('profile', AlunoProfileView.as_view(), name='aluno-profile'),
    path('avatar', AvatarUpdateView.as_view(), name='update-avatar'),
]
