from rest_framework import serializers
from .models import Challenge, UserChallenge

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')

class UserChallengeSerializer(serializers.ModelSerializer):
    challenge = ChallengeSerializer(read_only=True)
    
    class Meta:
        model = UserChallenge
        fields = '__all__'
        read_only_fields = ['user', 'submission_date', 'points_awarded']