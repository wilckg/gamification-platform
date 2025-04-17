from django.contrib import admin
from .models import Challenge, Question, Option

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True
    inlines = [OptionInline]

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'points', 'difficulty', 'challenge_type', 'created_by', 'is_active')
    list_filter = ('difficulty', 'is_active', 'challenge_type')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'points', 'difficulty', 'challenge_type')
        }),
        ('Datas', {
            'fields': ('start_date', 'end_date')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'challenge', 'order')
    list_filter = ('challenge',)
    inlines = [OptionInline]

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct', 'order')
    list_filter = ('question__challenge', 'is_correct')