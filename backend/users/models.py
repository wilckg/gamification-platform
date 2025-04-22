from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class CustomUser(AbstractUser):
    # Campos padrão modificados
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,  # Permite ser vazio para alunos
        null=True,
        help_text="Obrigatório apenas para administradores. Deixe em branco para alunos.",
    )
    email = models.EmailField(unique=True, verbose_name='email address')
    
    # Campos customizados
    points = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # Métodos
    def save(self, *args, **kwargs):
        if not self.is_staff and not self.username:  # Gera username só para alunos
            base_username = f"{slugify(self.first_name)}.{slugify(self.last_name)}"
            username = base_username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            self.username = username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username if self.username else f"{self.first_name} {self.last_name}"

    # Permissões (alunos não podem acessar o admin)
    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff