from django.contrib import admin
from .models import Track, Challenge, Question, Option, UserTrackProgress

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    fields = ['text', 'is_correct', 'order']

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True
    fields = ['text', 'order']
    inlines = [OptionInline]

class ChallengeInline(admin.TabularInline):
    model = Challenge
    extra = 1
    fields = ['title', 'description', 'points', 'difficulty', 'challenge_type', 'language', 'order']
    show_change_link = True

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    inlines = [ChallengeInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'icon', 'order')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'track', 'difficulty', 'challenge_type', 'language', 'is_active']
    list_filter = ['track', 'difficulty', 'challenge_type', 'is_active']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]
    fieldsets = (
        (None, {
            'fields': ('track', 'title', 'description', 'points', 'difficulty', 'challenge_type')
        }),
        ('Configurações de Código', {
            'fields': ('language',),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('start_date', 'end_date')
        }),
        ('Ordem', {
            'fields': ('order',)
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