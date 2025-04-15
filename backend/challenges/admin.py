from django.contrib import admin
from .models import Challenge

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'points', 'difficulty', 'created_by', 'is_active')
    list_filter = ('difficulty', 'is_active')
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'points', 'difficulty')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)