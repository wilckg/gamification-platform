from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Challenge, UserChallenge, Question, Option
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
    
    def create(self, request, *args, **kwargs):
        challenge_id = request.data.get('challenge')
        try:
            challenge = Challenge.objects.get(id=challenge_id)
        except Challenge.DoesNotExist:
            return Response(
                {'error': 'Desafio não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verifica se o usuário já respondeu esse desafio
        if UserChallenge.objects.filter(user=request.user, challenge=challenge).exists():
            return Response(
                {'error': 'Você já respondeu este desafio.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Cria a submissão
        user_challenge = serializer.save(
            user=request.user,
            challenge=challenge,
            is_correct=self.check_answer(challenge, request.data)
        
        # Atualiza pontos se correto
        if user_challenge.is_correct:
            user = request.user
            user.points += challenge.points
            user.save()
            user_challenge.points_awarded = True
            user_challenge.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def check_answer(self, challenge, data):
        if challenge.challenge_type == Challenge.TYPE_DESCRIPTION:
            # Lógica para verificar resposta descritiva (pode ser manual ou automática)
            return True  # Implemente sua lógica de verificação
            
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

class ChallengeSubmissionViewSet(viewsets.ModelViewSet):
    queryset = ChallengeSubmission.objects.all()
    serializer_class = ChallengeSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        submission = serializer.save(user=self.request.user)
        self.check_badges(submission.user)

    def check_badges(self, user):
        # Lógica para verificar conquistas
        total_points = user.points
        badges = Badge.objects.filter(points_required__lte=total_points)
        
        for badge in badges:
            if not UserBadge.objects.filter(user=user, badge=badge).exists():
                UserBadge.objects.create(user=user, badge=badge)

class RankingView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-points')
    serializer_class = UserSerializer
    pagination_class = None

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