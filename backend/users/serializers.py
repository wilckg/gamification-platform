from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class AlunoRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'username': {'required': False}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=False  # Garante que é aluno
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_staff:
            raise serializers.ValidationError("Apenas administradores podem fazer login aqui.")
        return data

class AlunoTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # Alunos usam email para login

    def validate(self, attrs):
        attrs['username'] = attrs.pop('email')  # Converte email para username
        data = super().validate(attrs)
        if self.user.is_staff:
            raise serializers.ValidationError("Use o painel de admin para login de administradores.")
        return data