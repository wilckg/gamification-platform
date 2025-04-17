from rest_framework import serializers
from .models import Challenge, UserChallenge, Question, Option

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
        read_only_fields = ['user', 'submission_date', 'points_awarded', 'is_correct']
    
    def validate(self, data):
        challenge = self.context['challenge']
        
        if challenge.challenge_type == Challenge.TYPE_DESCRIPTION and not data.get('answer'):
            raise serializers.ValidationError("Resposta descritiva é obrigatória para este tipo de desafio")
        
        if challenge.challenge_type in [Challenge.TYPE_SINGLE_CHOICE, Challenge.TYPE_MULTIPLE_CHOICE]:
            selected_options = data.get('selected_options', [])
            if not selected_options:
                raise serializers.ValidationError("Selecione pelo menos uma opção")
            
            if challenge.challenge_type == Challenge.TYPE_SINGLE_CHOICE and len(selected_options) > 1:
                raise serializers.ValidationError("Este desafio permite apenas uma resposta")
        
        return data