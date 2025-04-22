from rest_framework import serializers
from .models import Track, Challenge, Question, Option, UserChallenge, UserTrackProgress

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct', 'order']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'order', 'options']

class ChallengeSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Challenge
        fields = [
            'id', 'title', 'description', 'points', 'difficulty',
            'challenge_type', 'language', 'starter_code', 'solution_code',
            'expected_output', 'questions', 'is_active', 'order'
        ]
        read_only_fields = ('created_by',)

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
    
    def get_status_display(self, obj):
        return obj.get_status_display()

    def validate(self, data):
        challenge = self.context.get('challenge')
        
        if not challenge:
            raise serializers.ValidationError("Desafio não encontrado")
        
        # Validação específica por tipo de desafio
        if challenge.challenge_type == Challenge.TYPE_DESCRIPTION:
            if not data.get('answer'):
                raise serializers.ValidationError("Resposta descritiva é obrigatória")
        
        elif challenge.challenge_type == Challenge.TYPE_CODE:
            if not data.get('code'):
                raise serializers.ValidationError("Código é obrigatório")
        
        elif challenge.challenge_type in [Challenge.TYPE_SINGLE_CHOICE, Challenge.TYPE_MULTIPLE_CHOICE]:
            selected_options = data.get('selected_options', [])
            if not selected_options:
                raise serializers.ValidationError("Selecione pelo menos uma opção")
            
            if challenge.challenge_type == Challenge.TYPE_SINGLE_CHOICE and len(selected_options) > 1:
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