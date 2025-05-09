from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from .models import Track, Challenge, UserChallenge, UserTrackProgress, Question, Option
from .serializers import (
    TrackSerializer, ChallengeSerializer,
    ChallengeDetailSerializer,
    QuestionSerializer, OptionSerializer,
    UserChallengeSerializer, UserTrackProgressSerializer
)
from django.utils import timezone

class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.filter(is_active=True)
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChallengeDetailSerializer
        return ChallengeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Challenge.objects.filter(is_active=True)
        track_id = self.request.query_params.get('track_id')
        if track_id:
            queryset = queryset.filter(track_id=track_id)
        return queryset

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        challenge_id = self.request.query_params.get('challenge_id')
        if challenge_id:
            queryset = queryset.filter(challenge_id=challenge_id)
        return queryset

    @action(detail=False, methods=['get'], url_path='by-challenge/(?P<challenge_pk>[^/.]+)')
    def list_by_challenge(self, request, challenge_pk=None):
        questions = self.get_queryset().filter(challenge_id=challenge_pk)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        question_id = self.request.query_params.get('question_id')
        if question_id:
            queryset = queryset.filter(question_id=question_id)
        return queryset

    @action(detail=False, methods=['get'], url_path='by-question/(?P<question_pk>[^/.]+)')
    def list_by_question(self, request, question_pk=None):
        options = self.get_queryset().filter(question_id=question_pk)
        serializer = self.get_serializer(options, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

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
        
        # Verifica se o desafio está ativo
        if not challenge.is_active:
            raise ValidationError("Este desafio não está disponível no momento")
        
        # Verifica se o usuário já completou o desafio
        existing_submission = UserChallenge.objects.filter(
            user=request.user, 
            challenge=challenge
        ).first()
        
        if existing_submission:
            return Response(
                {'error': 'Você já respondeu este desafio.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data, context={'challenge': challenge})
        serializer.is_valid(raise_exception=True)
        
        # Processa a submissão
        user_challenge = serializer.save(
            user=request.user,
            challenge=challenge,
            status='PENDING'
        )
        
        # Avaliação automática baseada no tipo de desafio
        self.evaluate_submission(user_challenge)
        
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
    
    def evaluate_submission(self, user_challenge):
        challenge = user_challenge.challenge
        
        if challenge.challenge_type in ['SINGLE_CHOICE', 'MULTIPLE_CHOICE']:
            self.evaluate_quiz(user_challenge)
        elif challenge.challenge_type == 'CODE':
            self.evaluate_code(user_challenge)

    def evaluate_quiz(self, user_challenge):
        challenge = user_challenge.challenge
        selected_ids = list(user_challenge.selected_options.values_list('id', flat=True))
        correct_ids = list(Option.objects.filter(
            question__challenge=challenge,
            is_correct=True
        ).values_list('id', flat=True))
        
        if challenge.challenge_type == 'SINGLE_CHOICE':
            is_correct = len(selected_ids) == 1 and selected_ids[0] in correct_ids
        else:  # MULTIPLE_CHOICE
            is_correct = set(selected_ids) == set(correct_ids)
        
        user_challenge.status = 'CORRECT' if is_correct else 'INCORRECT'
        user_challenge.is_correct = is_correct
        user_challenge.obtained_points = challenge.points if is_correct else 0
        user_challenge.save()
        
        if is_correct:
            self.update_user_progress(user_challenge.user, challenge)

    def evaluate_code(self, user_challenge):
        # Implementação simplificada - você pode integrar com um serviço externo
        challenge = user_challenge.challenge
        try:
            # Simulação de execução de código
            user_challenge.code_output = "Saída simulada do código"
            
            # Verificação básica (em produção, use testes unitários)
            is_correct = True  # Substitua por lógica real de avaliação
            
            user_challenge.status = 'CORRECT' if is_correct else 'INCORRECT'
            user_challenge.is_correct = is_correct
            user_challenge.obtained_points = challenge.points if is_correct else 0
            user_challenge.feedback = "Código executado com sucesso" if is_correct else "Erro na execução"
            user_challenge.save()
            
            if is_correct:
                self.update_user_progress(user_challenge.user, challenge)
                
        except Exception as e:
            user_challenge.status = 'INCORRECT'
            user_challenge.feedback = f"Erro: {str(e)}"
            user_challenge.save()
    
    def update_user_progress(self, user, challenge):
        # Atualiza pontos do usuário
        user.points += challenge.points
        user.save()
        
        # Atualiza progresso na trilha
        track = challenge.track
        progress, created = UserTrackProgress.objects.get_or_create(
            user=user,
            track=track
        )
        
        if not progress.completed_challenges.filter(id=challenge.id).exists():
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
    
    @action(detail=False, methods=['get'], url_path='current')
    def current_progress(self, request):
        """Retorna todas as trilhas ativas com ou sem progresso, ordenadas por progresso decrescente"""
        tracks = Track.objects.filter(is_active=True)
        result = []

        for track in tracks:
            # Busca ou inicializa o progresso
            progress_obj = UserTrackProgress.objects.filter(user=request.user, track=track).first()

            if progress_obj:
                completed = progress_obj.completed_challenges.count()
            else:
                completed = 0

            total = track.challenges.count()
            percentage = int((completed / total) * 100) if total > 0 else 0

            # Serializa os dados da trilha como resposta única
            result.append({
                'id': progress_obj.id if progress_obj else None,
                'track': TrackSerializer(track, context=self.get_serializer_context()).data,
                'progress': {
                    'completed': completed,
                    'total': total,
                    'percentage': percentage
                },
                'is_completed': progress_obj.is_completed if progress_obj else False,
                'completed_at': progress_obj.completed_at if progress_obj else None,
                'progress_percentage': percentage
            })

        # Ordena trilhas com mais progresso primeiro
        result.sort(key=lambda x: x['progress_percentage'], reverse=True)

        return Response(result)
    
    @action(detail=True, methods=['get'])
    def challenges(self, request, pk=None):
        progress = self.get_object()
        challenges = progress.track.challenges.all()
        
        # Adiciona status de conclusão para cada desafio
        challenges_data = []
        for challenge in challenges:
            submission = UserChallenge.objects.filter(
                user=request.user,
                challenge=challenge
            ).first()
            
            challenge_data = ChallengeSerializer(challenge).data
            challenge_data['completed'] = submission.is_correct if submission else False
            challenge_data['submission_status'] = submission.status if submission else None
            challenges_data.append(challenge_data)
        
        return Response(challenges_data)