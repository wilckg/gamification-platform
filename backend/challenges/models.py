from django.db import models
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class Track(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)  # Para ícones (ex: 'FaPython')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Challenge(models.Model):
    TYPE_DESCRIPTION = 'D'
    TYPE_CODE = 'C'
    TYPE_SINGLE_CHOICE = 'S'
    TYPE_MULTIPLE_CHOICE = 'M'
    TYPE_CHOICES = [
        (TYPE_DESCRIPTION, 'Descrição'),
        (TYPE_CODE, 'Código'),
        (TYPE_SINGLE_CHOICE, 'Escolha Única'),
        (TYPE_MULTIPLE_CHOICE, 'Múltipla Escolha'),
    ]
    
    DIFFICULTY_EASY = 'E'
    DIFFICULTY_MEDIUM = 'M'
    DIFFICULTY_HARD = 'H'
    DIFFICULTY_CHOICES = [
        (DIFFICULTY_EASY, 'Fácil'),
        (DIFFICULTY_MEDIUM, 'Médio'),
        (DIFFICULTY_HARD, 'Difícil'),
    ]
    
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='challenges')
    # track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='challenges', null=True)  # Temporário
    title = models.CharField(max_length=255)
    description = models.TextField()
    points = models.IntegerField()
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    challenge_type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    language = models.CharField(max_length=50, blank=True, null=True)  # Para desafios de código
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.track.title} - {self.title}"

class Question(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']

class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_submissions')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='user_submissions')
    submission_date = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(blank=True, null=True)  # Para respostas descritivas
    code = models.TextField(blank=True, null=True)  # Para respostas de código
    selected_options = models.ManyToManyField(Option, blank=True)  # Para respostas de quiz
    is_correct = models.BooleanField(default=False)
    points_awarded = models.BooleanField(default=False)
    feedback = models.TextField(blank=True, null=True)  # Feedback para respostas de código
    
    class Meta:
        unique_together = ('user', 'challenge')
        ordering = ['-submission_date']

class UserTrackProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='track_progress')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='user_progress')
    completed_challenges = models.ManyToManyField(Challenge, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'track')