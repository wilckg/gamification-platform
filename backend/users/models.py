from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class CustomUser(AbstractUser):
    # Campos para administradores
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text="Obrigatório apenas para administradores. Deixe em branco para alunos."
    )
    
    # Campos para todos
    email = models.EmailField(unique=True, verbose_name='email address')
    first_name = models.CharField(max_length=150, verbose_name='first name')
    last_name = models.CharField(max_length=150, verbose_name='last name')
    
    # Campos customizados
    points = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_aluno = models.BooleanField(default=False, verbose_name='É aluno?')

    # Configurações
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        # Lógica para alunos
        if not self.is_staff and not self.is_superuser:
            self.is_aluno = True
            if not self.username:
                base_username = f"{slugify(self.first_name)}.{slugify(self.last_name)}"
                username = base_username
                counter = 1
                while CustomUser.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                self.username = username
        
        # Lógica para administradores
        elif self.is_staff and not self.username:
            raise ValueError("Administradores devem ter um username")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({'Admin' if self.is_staff else 'Aluno'})"

    # Permissões
    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff