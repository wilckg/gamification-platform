from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from enum import Enum

User = get_user_model()

# Enum para tipos de desafio
class ChallengeType(Enum):
    DESCRIPTION = "DESCRIPTION"
    CODE = "CODE"
    SINGLE_CHOICE = "SINGLE_CHOICE"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ').title()) for key in cls]

    @classmethod
    def get_display_name(cls, value):
        return dict(cls.choices()).get(value, value)

# Enum para dificuldade
class DifficultyLevel(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

    @classmethod
    def choices(cls):
        return [(key.value, key.name.title()) for key in cls]

class Track(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Título"))
    description = models.TextField(verbose_name=_("Descrição"))
    icon = models.CharField(max_length=50, blank=True, verbose_name=_("Ícone"))
    is_active = models.BooleanField(default=True, verbose_name=_("Ativo?"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordem"))
    
    class Meta:
        verbose_name = _("Trilha")
        verbose_name_plural = _("Trilhas")
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Challenge(models.Model):
    track = models.ForeignKey(
        Track, 
        on_delete=models.CASCADE, 
        related_name='challenges',
        verbose_name=_("Trilha")
    )
    title = models.CharField(max_length=255, verbose_name=_("Título"))
    description = models.TextField(verbose_name=_("Descrição"))
    points = models.IntegerField(verbose_name=_("Pontos"))
    difficulty = models.CharField(
        max_length=10,
        choices=DifficultyLevel.choices(),
        default=DifficultyLevel.EASY.value,
        verbose_name=_("Dificuldade")
    )
    challenge_type = models.CharField(
        max_length=20,
        choices=ChallengeType.choices(),
        default=ChallengeType.CODE.value,
        verbose_name=_("Tipo de Desafio")
    )
    language = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name=_("Linguagem de Programação")
    )
    starter_code = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_("Código Inicial"),
        help_text=_("Código inicial para desafios de programação")
    )
    solution_code = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_("Código Solução"),
        help_text=_("Solução esperada para desafios de código")
    )
    expected_output = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_("Saída Esperada"),
        help_text=_("Saída esperada para desafios de código")
    )
    start_date = models.DateTimeField(
        null=True,
        blank=True,
        default=timezone.now,
        verbose_name=_("Data de Início")
    )
    end_date = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name=_("Data de Término")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Ativo?")
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Ordem")
    )
    
    
    class Meta:
        verbose_name = _("Desafio")
        verbose_name_plural = _("Desafios")
        ordering = ['order']
    
    @property
    def TYPE_DESCRIPTION(self):
        return ChallengeType.DESCRIPTION.value
    
    @property
    def TYPE_CODE(self):
        return ChallengeType.CODE.value
    
    @property
    def TYPE_SINGLE_CHOICE(self):
        return ChallengeType.SINGLE_CHOICE.value
    
    @property
    def TYPE_MULTIPLE_CHOICE(self):
        return ChallengeType.MULTIPLE_CHOICE.value

    def __str__(self):
        return f"{self.track.title} - {self.title}"
    
    def get_challenge_type_display(self):
        return ChallengeType.get_display_name(self.challenge_type)

class Question(models.Model):
    challenge = models.ForeignKey(
        Challenge, 
        on_delete=models.CASCADE, 
        related_name='questions',
        verbose_name=_("Desafio")
    )
    text = models.TextField(verbose_name=_("Texto da Questão"))
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Ordem")
    )
    
    class Meta:
        verbose_name = _("Questão")
        verbose_name_plural = _("Questões")
        ordering = ['order']

class Option(models.Model):
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name='options',
        verbose_name=_("Questão")
    )
    text = models.TextField(verbose_name=_("Texto da Opção"))
    is_correct = models.BooleanField(
        default=False,
        verbose_name=_("Está Correta?")
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Ordem")
    )
    
    class Meta:
        verbose_name = _("Opção")
        verbose_name_plural = _("Opções")
        ordering = ['order']

class UserChallenge(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pendente')
        CORRECT = 'CORRECT', _('Correto')
        INCORRECT = 'INCORRECT', _('Incorreto')
        PARTIAL = 'PARTIAL', _('Parcialmente Correto')
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='challenge_submissions',
        verbose_name=_("Usuário")
    )
    challenge = models.ForeignKey(
        Challenge, 
        on_delete=models.CASCADE, 
        related_name='user_submissions',
        verbose_name=_("Desafio")
    )
    submission_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Data de Submissão")
    )
    answer = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_("Resposta Descritiva")
    )
    code = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_("Código Submetido")
    )
    selected_options = models.ManyToManyField(
        Option, 
        blank=True,
        verbose_name=_("Opções Selecionadas")
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name=_("Está Correto?")
    )
    points_awarded = models.BooleanField(
        default=False,
        verbose_name=_("Pontos Atribuídos?")
    )
    feedback = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_("Feedback")
    )
    code_output = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_("Saída do Código")
    )
    obtained_points = models.IntegerField(
        default=0,
        verbose_name=_("Pontos Obtidos")
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Status")
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Submetido em")
    )
    evaluated_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name=_("Avaliado em")
    )
    
    class Meta:
        verbose_name = _("Submissão de Desafio")
        verbose_name_plural = _("Submissões de Desafios")
        ordering = ['-submitted_at']
        unique_together = ('user', 'challenge')

class UserTrackProgress(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='track_progress',
        verbose_name=_("Usuário")
    )
    track = models.ForeignKey(
        Track, 
        on_delete=models.CASCADE, 
        related_name='user_progress',
        verbose_name=_("Trilha")
    )
    completed_challenges = models.ManyToManyField(
        Challenge, 
        blank=True,
        verbose_name=_("Desafios Completados")
    )
    completed_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name=_("Completado em")
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name=_("Completo?")
    )
    
    class Meta:
        verbose_name = _("Progresso na Trilha")
        verbose_name_plural = _("Progressos nas Trilhas")
        unique_together = ('user', 'track')