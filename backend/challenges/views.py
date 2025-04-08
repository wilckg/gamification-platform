# backend/challenges/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Challenge, UserChallenge
from .serializers import ChallengeSerializer, UserChallengeSerializer
from users.models import CustomUser

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.filter(is_active=True)
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class UserChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = UserChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserChallenge.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        challenge_id = self.request.data.get('challenge')
        challenge = Challenge.objects.get(id=challenge_id)
        
        # Verifica se o usuário já respondeu esse desafio
        if UserChallenge.objects.filter(user=self.request.user, challenge=challenge).exists():
            return Response(
                {'error': 'You have already submitted an answer for this challenge.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_challenge = serializer.save(user=self.request.user, challenge=challenge)
        
        # Aqui você implementaria a lógica para verificar a resposta
        # Por simplicidade, vamos assumir que todas as respostas estão corretas
        user_challenge.is_correct = True
        user_challenge.save()
        
        # Atualiza os pontos do usuário
        user = self.request.user
        user.points += challenge.points
        user.save()

class RankingViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    def list(self, request):
        users = CustomUser.objects.all().order_by('-points')
        serializer = UserSerializer(users, many=True)
        
        # Adiciona a posição no ranking
        ranked_data = []
        for index, user_data in enumerate(serializer.data, start=1):
            user_data['position'] = index
            ranked_data.append(user_data)
        
        return Response(ranked_data)