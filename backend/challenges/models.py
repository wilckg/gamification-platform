# backend/challenges/models.py
from django.db import models
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

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
        
class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/')
    points_required = models.IntegerField(default=0)

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(auto_now_add=True)

class ChallengeSubmission(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    answer = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    submitted_at = models.DateTimeField(auto_now_add=True)
    points_awarded = models.IntegerField(default=0)