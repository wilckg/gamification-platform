from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)

    # Campos para edição
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informações Pessoais'), {'fields': ('email', 'first_name', 'last_name', 'profile_picture', 'points')}),
        (_('Permissões'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Campos para criação (diferencia admin/aluno)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff'),
        }),
    )

    def get_fields(self, request, obj=None):
        if obj and not obj.is_staff:  # Oculta username para alunos
            return [f.name for f in self.model._meta.fields if f.name != 'username'] + ['password']
        return super().get_fields(request, obj)

admin.site.register(CustomUser, CustomUserAdmin)