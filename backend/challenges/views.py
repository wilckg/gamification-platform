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
from users.models import CustomUser

# ---------- TRACK ----------
class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.filter(is_active=True)
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# ---------- CHALLENGE ----------
class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return ChallengeDetailSerializer if self.action == 'retrieve' else ChallengeSerializer

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

# ---------- QUESTION ----------
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        challenge_id = self.request.query_params.get('challenge_id')
        return self.queryset.filter(challenge_id=challenge_id) if challenge_id else self.queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

# ---------- OPTION ----------
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

# ---------- USER CHALLENGE ----------
class UserChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = UserChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserChallenge.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        print("\n🚀 INÍCIO DA SUBMISSÃO")

        try:
            # Desafio vindo do payload
            challenge_id = request.data.get('challenge')
            print("🔍 ID do desafio recebido:", challenge_id)

            if not challenge_id:
                print("❌ Erro: ID do desafio ausente.")
                return Response({'error': 'ID do desafio é obrigatório.'}, status=400)

            challenge = Challenge.objects.filter(id=challenge_id).first()
            if not challenge:
                print(f"❌ Erro: Desafio ID {challenge_id} não encontrado.")
                return Response({'error': f'Desafio com ID {challenge_id} não encontrado.'}, status=404)

            print("✅ Desafio encontrado:", challenge)

            if not challenge.is_active:
                print("⚠️ Desafio está inativo.")
                return Response({'error': 'Este desafio está inativo.'}, status=400)

            user = request.user
            print("👤 Usuário autenticado:", user, type(user))

            if UserChallenge.objects.filter(user=user, challenge=challenge).exists():
                print("⚠️ Usuário já submeteu esse desafio.")
                return Response({'error': 'Você já respondeu este desafio.'}, status=400)

            # Agora que tudo está validado, vamos pro serializer
            serializer = self.get_serializer(data=request.data, context={'challenge': challenge})

            if not serializer.is_valid():
                print("❌ ERRO DE VALIDAÇÃO:")
                print("📦 Payload recebido:", request.data)
                print("🧪 Erros de validação:", serializer.errors)
                return Response(serializer.errors, status=400)

            validated_data = serializer.validated_data.copy()
            selected_options = validated_data.pop('selected_options', [])
            challenge = validated_data.pop('challenge')

            print("✅ Dados validados:")
            print("  selected_options:", [opt.id for opt in selected_options])
            print("  restante:", validated_data)

            # Verifica se opções realmente pertencem ao desafio
            invalid_options = [
                opt.id for opt in selected_options
                if opt.question.challenge_id != challenge.id
            ]
            if invalid_options:
                print("❌ Opções inválidas detectadas:", invalid_options)
                return Response(
                    {'error': f'As opções {invalid_options} não pertencem ao desafio {challenge.id}.'},
                    status=400
                )

            now = timezone.now()
            user_challenge = UserChallenge.objects.create(
                user=user,
                challenge=challenge,
                submission_date=now,
                submitted_at=now,
                status='PENDING',
                is_correct=False,
                obtained_points=0,
                **validated_data
            )
            user_challenge.selected_options.set(selected_options)

            print("✅ UserChallenge criado com ID:", user_challenge.id)

            self.evaluate_submission(user_challenge)

            return Response(self.get_serializer(user_challenge).data, status=201)

        except Exception as e:
            import traceback
            print("❌ EXCEÇÃO FATAL:")
            traceback.print_exc()
            return Response({'error': f'Erro inesperado: {str(e)}'}, status=500)

    def evaluate_submission(self, user_challenge):
        challenge = user_challenge.challenge
        data = {
            'code': user_challenge.code,
            'answer': user_challenge.answer,
            'selected_options': list(user_challenge.selected_options.all().values_list('id', flat=True)),
        }

        is_correct = self.check_answer(challenge, data)

        user_challenge.status = 'CORRECT' if is_correct else 'INCORRECT'
        user_challenge.is_correct = is_correct
        user_challenge.obtained_points = challenge.points if is_correct else 0
        user_challenge.feedback = "Resposta correta!" if is_correct else "Resposta incorreta."
        user_challenge.evaluated_at = timezone.now()
        user_challenge.save()

        if is_correct:
            self.update_user_progress(user_challenge.user, challenge)

    def check_answer(self, challenge, data):
        if challenge.challenge_type == challenge.TYPE_CODE:
            return True  # avaliação fictícia
        elif challenge.challenge_type == challenge.TYPE_DESCRIPTION:
            return True
        elif challenge.challenge_type in [challenge.TYPE_SINGLE_CHOICE, challenge.TYPE_MULTIPLE_CHOICE]:
            selected_ids = set(data.get('selected_options', []))
            correct_ids = set(
                Option.objects.filter(question__challenge=challenge, is_correct=True).values_list('id', flat=True)
            )
            return selected_ids == correct_ids
        return False

    def update_user_progress(self, user, challenge):
        user.points += challenge.points
        user.save()

        track = challenge.track
        progress, _ = UserTrackProgress.objects.get_or_create(user=user, track=track)

        if not progress.completed_challenges.filter(id=challenge.id).exists():
            progress.completed_challenges.add(challenge)

            total = track.challenges.count()
            completed = progress.completed_challenges.count()
            if completed >= total:
                progress.is_completed = True
                progress.completed_at = timezone.now()
            progress.save()

# ---------- USER TRACK PROGRESS ----------
class UserTrackProgressViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserTrackProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserTrackProgress.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='current')
    def current_progress(self, request):
        tracks = Track.objects.filter(is_active=True)
        result = []

        for track in tracks:
            progress_obj = UserTrackProgress.objects.filter(user=request.user, track=track).first()
            completed = progress_obj.completed_challenges.count() if progress_obj else 0
            total = track.challenges.count()
            percentage = int((completed / total) * 100) if total > 0 else 0

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

        result.sort(key=lambda x: x['progress_percentage'], reverse=True)
        return Response(result)

    @action(detail=True, methods=['get'])
    def challenges(self, request, pk=None):
        progress = self.get_object()
        challenges = progress.track.challenges.all()
        return Response({'challenges': [c.id for c in challenges]})
