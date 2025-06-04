from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

from django.core.validators import MinValueValidator
from django.conf import settings


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")
        email = self.normalize_email(email)

        # Geração automática de username se não for informado
        if not extra_fields.get("username"):
            extra_fields["username"] = self.generate_unique_username()

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("username"):
            raise ValidationError("Administradores precisam de um username manualmente definido.")

        return self.create_user(email, password, **extra_fields)

    def generate_unique_username(self):
        base_username = get_random_string(8).lower()
        while self.model.objects.filter(username=base_username).exists():
            base_username = get_random_string(8).lower()
        return base_username


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email"), unique=True)
    username = models.CharField(_("nome de usuário"), max_length=150, unique=True)
    first_name = models.CharField(_("nome"), max_length=150)
    last_name = models.CharField(_("sobrenome"), max_length=150)
    is_staff = models.BooleanField(_("admin do sistema?"), default=False)
    is_active = models.BooleanField(_("ativo?"), default=True)
    date_joined = models.DateTimeField(_("data de entrada"), default=timezone.now)
    is_aluno = models.BooleanField(_("é aluno?"), default=False)

    # ✅ Novos campos:
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        null=True,
        blank=True,
        verbose_name=_("foto de perfil")
    )
    points = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("pontuação")
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = _("usuário")
        verbose_name_plural = _("usuários")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"