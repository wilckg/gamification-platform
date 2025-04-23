from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_aluno')
    list_filter = ('is_staff', 'is_aluno', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')

    # Campos para edição
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informações Pessoais'), {'fields': ('first_name', 'last_name', 'profile_picture', 'points')}),
        (_('Permissões'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_aluno', 'groups', 'user_permissions'),
            'description': _("Marque 'is_staff' para administradores e 'is_aluno' para estudantes")
        }),
    )

    # Campos para criação
    add_fieldsets = (
        ('Administrador', {
            'classes': ('collapse',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser'),
            'description': _('Use esta seção para criar novos administradores')
        }),
        ('Aluno', {
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
            'description': _('Use esta seção para criar novos alunos')
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

admin.site.register(CustomUser, CustomUserAdmin)