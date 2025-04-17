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
        fields = '__all__'
        read_only_fields = ('created_by',)

class TrackSerializer(serializers.ModelSerializer):
    challenges = ChallengeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Track
        fields = '__all__'

class UserChallengeSerializer(serializers.ModelSerializer):
    challenge = ChallengeSerializer(read_only=True)
    selected_options = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Option.objects.all(),
        required=False
    )
    
    class Meta:
        model = UserChallenge
        fields = '__all__'
        read_only_fields = ['user', 'submission_date', 'points_awarded', 'is_correct', 'feedback']
    
    def validate(self, data):
        challenge = self.context.get('challenge')
        
        if not challenge:
            raise serializers.ValidationError("Desafio não encontrado")
        
        if challenge.challenge_type in [Challenge.TYPE_DESCRIPTION, Challenge.TYPE_CODE] and not data.get('answer') and not data.get('code'):
            raise serializers.ValidationError("Resposta é obrigatória para este tipo de desafio")
        
        if challenge.challenge_type in [Challenge.TYPE_SINGLE_CHOICE, Challenge.TYPE_MULTIPLE_CHOICE]:
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