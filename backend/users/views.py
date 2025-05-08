from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from .serializers import (
    AlunoSerializer,
    AdminSerializer,
    AdminTokenObtainPairSerializer,
    AlunoTokenObtainPairSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    AvatarSerializer
)

User = get_user_model()

class AdminCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(is_staff=True)

class AlunoCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(is_aluno=True)

class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

class AlunoTokenObtainPairView(TokenObtainPairView):
    serializer_class = AlunoTokenObtainPairSerializer

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            
            send_mail(
                'Redefinição de Senha',
                f'Use este link para redefinir sua senha: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        
        return Response(
            {'detail': 'Se o e-mail existir, um link de redefinição foi enviado'},
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uidb64']))
            user = User.objects.get(pk=uid)
            
            if default_token_generator.check_token(user, serializer.validated_data['token']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response(
                    {'detail': 'Senha redefinida com sucesso'},
                    status=status.HTTP_200_OK
                )
        
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            pass
            
        return Response(
            {'detail': 'Link inválido ou expirado'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
class AlunoProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AlunoSerializer(request.user)
        return Response(serializer.data)

class AvatarUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = AvatarSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)