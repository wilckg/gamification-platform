from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserChallenge
from django.utils import timezone

@receiver(post_save, sender=UserChallenge)
def update_user_points(sender, instance, created, **kwargs):
    if instance.status == UserChallenge.STATUS_CORRECT and not instance.points_awarded:
        instance.user.points += instance.challenge.points
        instance.user.save()
        instance.points_awarded = True
        instance.evaluated_at = timezone.now()
        instance.save()
        
        # Atualiza progresso na trilha
        track = instance.challenge.track
        progress, created = UserTrackProgress.objects.get_or_create(
            user=instance.user,
            track=track
        )
        
        if not progress.completed_challenges.filter(id=instance.challenge.id).exists():
            progress.completed_challenges.add(instance.challenge)
            
            # Verifica se completou a trilha
            total_challenges = track.challenges.count()
            completed = progress.completed_challenges.count()
            
            if completed >= total_challenges:
                progress.is_completed = True
                progress.completed_at = timezone.now()
                progress.save()