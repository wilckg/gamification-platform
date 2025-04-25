from rest_framework import serializers
from .models import Track, Challenge, Question, Option, UserChallenge, UserTrackProgress

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct', 'order', 'question']
        extra_kwargs = {
            'question': {'required': True}
        }

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'order', 'challenge']
        extra_kwargs = {
            'challenge': {'required': True}
        }

class ChallengeSerializer(serializers.ModelSerializer):
    track = serializers.PrimaryKeyRelatedField(queryset=Track.objects.all())
    
    class Meta:
        model = Challenge
        fields = [
            'id', 'track', 'title', 'description', 'points', 'difficulty',
            'challenge_type', 'language', 'starter_code', 'solution_code',
            'expected_output', 'is_active', 'order'
        ]
        extra_kwargs = {
            'track': {'required': True}
        }

class TrackSerializer(serializers.ModelSerializer):
    challenges = ChallengeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Track
        fields = '__all__'

class UserChallengeSerializer(serializers.ModelSerializer):
    challenge = ChallengeSerializer(read_only=True)
    selected_options = OptionSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = UserChallenge
        fields = [
            'id', 'user', 'challenge', 'submission_date', 'answer', 'code',
            'selected_options', 'status', 'status_display', 'is_correct',
            'points_awarded', 'feedback', 'code_output', 'obtained_points'
        ]
        read_only_fields = [
            'user', 'submission_date', 'status', 'is_correct',
            'points_awarded', 'feedback', 'code_output', 'obtained_points'
        ]
    
    def validate(self, data):
        challenge = self.context.get('challenge')
        
        if not challenge:
            raise serializers.ValidationError("Desafio não encontrado")
        
        # Validação específica por tipo de desafio
        if challenge.challenge_type == "DESCRIPTION":
            if not data.get('answer'):
                raise serializers.ValidationError("Resposta descritiva é obrigatória")
        
        elif challenge.challenge_type == "CODE":
            if not data.get('code'):
                raise serializers.ValidationError("Código é obrigatório")
        
        elif challenge.challenge_type in ["SINGLE_CHOICE", "MULTIPLE_CHOICE"]:
            selected_options = data.get('selected_options', [])
            if not selected_options:
                raise serializers.ValidationError("Selecione pelo menos uma opção")
            
            if challenge.challenge_type == "SINGLE_CHOICE" and len(selected_options) > 1:
                raise serializers.ValidationError("Este desafio permite apenas uma resposta")
        
        return data

class UserTrackProgressSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = UserTrackProgress
        fields = '__all__'
    
    def get_progress(self, obj):
        total_challenges = obj.track.challenges.count()
        completed = obj.completed_challenges.count()
        return {
            'completed': completed,
            'total': total_challenges,
            'percentage': int((completed / total_challenges) * 100) if total_challenges > 0 else 0
        }