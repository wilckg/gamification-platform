from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import UserChallenge, UserTrackProgress

@receiver(post_save, sender=UserChallenge)
def update_user_points(sender, instance, created, **kwargs):
    # Apenas processa se ainda não recebeu os pontos
    if instance.status in [UserChallenge.Status.CORRECT, UserChallenge.Status.PARTIAL] and not instance.points_awarded:
        # ✅ Soma os pontos obtidos individualmente
        instance.user.points += instance.obtained_points
        instance.user.save()

        instance.points_awarded = True
        instance.evaluated_at = timezone.now()
        instance.save()

        # ✅ Atualiza progresso da trilha
        track = instance.challenge.track
        progress, _ = UserTrackProgress.objects.get_or_create(
            user=instance.user,
            track=track
        )

        # Adiciona desafio se ainda não estiver associado
        if not progress.completed_challenges.filter(id=instance.challenge.id).exists():
            progress.completed_challenges.add(instance.challenge)

        # Verifica se todos os desafios da trilha foram resolvidos
        total_required = track.challenges.count()
        total_completed = progress.completed_challenges.count()

        if total_completed >= total_required:
            progress.is_completed = True
            progress.completed_at = timezone.now()

        progress.save()
