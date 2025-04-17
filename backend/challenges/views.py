from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Track, Challenge, UserChallenge, UserTrackProgress
from .serializers import (
    TrackSerializer, ChallengeSerializer, 
    UserChallengeSerializer, UserTrackProgressSerializer
)

class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.filter(is_active=True)
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Challenge.objects.filter(is_active=True)
        track_id = self.request.query_params.get('track_id')
        if track_id:
            queryset = queryset.filter(track_id=track_id)
        return queryset

class UserChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = UserChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserChallenge.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        challenge_id = request.data.get('challenge')
        try:
            challenge = Challenge.objects.get(id=challenge_id)
        except Challenge.DoesNotExist:
            return Response(
                {'error': 'Desafio não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if UserChallenge.objects.filter(user=request.user, challenge=challenge).exists():
            return Response(
                {'error': 'Você já respondeu este desafio.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data, context={'challenge': challenge})
        serializer.is_valid(raise_exception=True)
        
        user_challenge = serializer.save(
            user=request.user,
            challenge=challenge,
            is_correct=self.check_answer(challenge, request.data)
        
        if user_challenge.is_correct:
            self.update_progress(request.user, challenge)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def check_answer(self, challenge, data):
        if challenge.challenge_type == Challenge.TYPE_CODE:
            # Implemente lógica de avaliação de código
            return self.evaluate_code(data.get('code'), challenge.language)
        elif challenge.challenge_type == Challenge.TYPE_DESCRIPTION:
            return True  # Avaliação manual
        elif challenge.challenge_type in [Challenge.TYPE_SINGLE_CHOICE, Challenge.TYPE_MULTIPLE_CHOICE]:
            selected_option_ids = data.get('selected_options', [])
            correct_options = Option.objects.filter(
                question__challenge=challenge,
                is_correct=True
            ).values_list('id', flat=True)
            
            selected_options_set = set(selected_option_ids)
            correct_options_set = set(correct_options)
            
            if challenge.challenge_type == Challenge.TYPE_SINGLE_CHOICE:
                return len(selected_options_set) == 1 and selected_options_set.issubset(correct_options_set)
            else:
                return selected_options_set == correct_options_set
        return False
    
    def evaluate_code(self, code, language):
        # Implemente sua lógica de avaliação de código aqui
        # Pode integrar com serviços como Jobe, Piston API ou seu próprio executor
        return True  # Temporário
    
    def update_progress(self, user, challenge):
        # Atualiza pontos do usuário
        user.points += challenge.points
        user.save()
        
        # Atualiza progresso na trilha
        track = challenge.track
        progress, created = UserTrackProgress.objects.get_or_create(
            user=user,
            track=track
        )
        progress.completed_challenges.add(challenge)
        
        # Verifica se completou a trilha
        total_challenges = track.challenges.count()
        completed = progress.completed_challenges.count()
        if completed >= total_challenges:
            progress.is_completed = True
            progress.completed_at = timezone.now()
            progress.save()

class UserTrackProgressViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserTrackProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserTrackProgress.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def challenges(self, request, pk=None):
        progress = self.get_object()
        challenges = progress.track.challenges.all()
        serializer = ChallengeSerializer(challenges, many=True)
        return Response(serializer.data)