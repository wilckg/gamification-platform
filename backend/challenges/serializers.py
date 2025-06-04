from rest_framework import serializers
from .models import Track, Challenge, Question, Option, UserChallenge, UserTrackProgress

class OptionInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct', 'order']

class QuestionWithOptionsSerializer(serializers.ModelSerializer):
    options = OptionInlineSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'order', 'options']

class ChallengeDetailSerializer(serializers.ModelSerializer):
    questions = QuestionWithOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Challenge
        fields = [
            'id', 'track', 'title', 'description', 'points', 'difficulty',
            'challenge_type', 'language', 'starter_code', 'solution_code',
            'expected_output', 'is_active', 'order', 'questions'
        ]

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
    challenge = serializers.PrimaryKeyRelatedField(
        queryset=Challenge.objects.all(), write_only=True
    )
    selected_options = serializers.PrimaryKeyRelatedField(
        queryset=Option.objects.all(),
        many=True,
        required=False
    )
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
        # Usa desafio do contexto ou payload
        challenge = data.get('challenge') or self.context.get('challenge')
        if not challenge:
            raise serializers.ValidationError("Desafio não informado ou inválido.")

        challenge_type = challenge.challenge_type
        selected_options = data.get('selected_options', [])
        answer = data.get('answer', '')
        code = data.get('code', '')

        # Validação por tipo de desafio
        if challenge_type == Challenge.TYPE_DESCRIPTION:
            if not answer or not answer.strip():
                raise serializers.ValidationError({
                    "answer": "Resposta descritiva é obrigatória."
                })

        elif challenge_type == Challenge.TYPE_CODE:
            if not code or not code.strip():
                raise serializers.ValidationError({
                    "code": "Código é obrigatório."
                })

        elif challenge_type in [Challenge.TYPE_SINGLE_CHOICE, Challenge.TYPE_MULTIPLE_CHOICE]:
            if not selected_options:
                raise serializers.ValidationError({
                    "selected_options": "Pelo menos uma opção deve ser selecionada."
                })

            if challenge_type == Challenge.TYPE_SINGLE_CHOICE and len(selected_options) > 1:
                raise serializers.ValidationError({
                    "selected_options": "Apenas uma opção deve ser selecionada neste desafio."
                })

        else:
            raise serializers.ValidationError("Tipo de desafio não reconhecido.")

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
