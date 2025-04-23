from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

# 1. Criamos modelos proxy para a separação visual
class Administrador(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'

class Aluno(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

# 2. Admin customizado para Administradores
class AdministradorAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Informações Pessoais'), {'fields': ('first_name', 'last_name')}),
        (_('Permissões'), {
            'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.is_staff = True  # Garante que é staff
        if not obj.username:
            obj.username = obj.email  # Ou sua lógica para username
        super().save_model(request, obj, form, change)

# 3. Admin customizado para Alunos
class AlunoAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_aluno=True)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informações Pessoais'), {'fields': ('first_name', 'last_name', 'profile_picture', 'points')}),
        (_('Permissões'), {'fields': ('is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.is_aluno = True
        obj.is_staff = False  # Garante que não é staff
        if not obj.username:
            base_username = f"{obj.first_name.lower()}.{obj.last_name.lower()}".replace(' ', '')
            username = base_username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            obj.username = username
        super().save_model(request, obj, form, change)

# 4. Registramos os modelos proxy
admin.site.register(Administrador, AdministradorAdmin)
admin.site.register(Aluno, AlunoAdmin)

# 5. Opcional: Desregistrar o modelo original se não quiser duplicação
# admin.site.unregister(CustomUser)