# backend/challenges/models.py
from django.db import models
from users.models import CustomUser

class Challenge(models.Model):
    EASY = 'E'
    MEDIUM = 'M'
    HARD = 'H'
    DIFFICULTY_CHOICES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    points = models.IntegerField()
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_challenges')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class UserChallenge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_challenges')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='challenge_users')
    submission_date = models.DateTimeField(auto_now_add=True)
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    points_awarded = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'challenge')