from django.contrib import admin
from django.utils import timezone
from .models import Track, Challenge, Question, Option, UserChallenge, UserTrackProgress

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    fields = ['text', 'is_correct', 'order']
    ordering = ['order']

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True
    fields = ['text', 'order']
    ordering = ['order']
    inlines = [OptionInline]

class ChallengeInline(admin.TabularInline):
    model = Challenge
    extra = 1
    fields = ['title', 'description', 'points', 'difficulty', 'challenge_type', 'language', 'order']
    show_change_link = True
    ordering = ['order']

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    inlines = [ChallengeInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'icon', 'order')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at')
        }),
    )
    readonly_fields = ['created_at']

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'track', 'difficulty', 'challenge_type', 'language', 'is_active', 'order']
    list_filter = ['track', 'difficulty', 'challenge_type', 'is_active']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]
    fieldsets = (
        (None, {
            'fields': ('track', 'title', 'description', 'points', 'difficulty', 'challenge_type')
        }),
        ('Configurações de Código', {
            'fields': ('language', 'starter_code', 'solution_code', 'expected_output'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('start_date', 'end_date')
        }),
        ('Ordem e Status', {
            'fields': ('order', 'is_active')
        }),
    )
    ordering = ['track', 'order']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'challenge', 'order')
    list_filter = ('challenge', 'challenge__track')
    inlines = [OptionInline]
    ordering = ['challenge', 'order']
    search_fields = ['text']

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct', 'order')
    list_filter = ('question__challenge', 'is_correct')
    ordering = ['question', 'order']
    search_fields = ['text']

@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'status', 'is_correct', 'obtained_points', 'submission_date', 'evaluated_at']
    list_filter = ['status', 'is_correct', 'challenge__track', 'challenge__difficulty']
    readonly_fields = ['submission_date', 'evaluated_at']
    search_fields = ['user__username', 'challenge__title']
    list_select_related = ['user', 'challenge', 'challenge__track']
    actions = ['mark_as_correct', 'mark_as_incorrect', 'mark_as_partial']
    fieldsets = (
        (None, {
            'fields': ('user', 'challenge', 'status')
        }),
        ('Submissão', {
            'fields': ('answer', 'code', 'selected_options')
        }),
        ('Resultados', {
            'fields': ('is_correct', 'obtained_points', 'points_awarded', 'feedback', 'code_output')
        }),
        ('Datas', {
            'fields': ('submission_date', 'evaluated_at'),
            'classes': ('collapse',)
        }),
    )

    def mark_as_correct(self, request, queryset):
        for obj in queryset:
            obj.status = UserChallenge.STATUS_CORRECT
            obj.is_correct = True
            obj.obtained_points = obj.challenge.points
            obj.evaluated_at = timezone.now()
            obj.save()
            self.update_user_progress(obj.user, obj.challenge)
        self.message_user(request, f"{queryset.count()} submissões marcadas como corretas")
    mark_as_correct.short_description = "Marcar como correto"

    def mark_as_incorrect(self, request, queryset):
        updated = queryset.update(
            status=UserChallenge.STATUS_INCORRECT,
            is_correct=False,
            obtained_points=0,
            evaluated_at=timezone.now()
        )
        self.message_user(request, f"{updated} submissões marcadas como incorretas")
    mark_as_incorrect.short_description = "Marcar como incorreto"

    def mark_as_partial(self, request, queryset):
        for obj in queryset:
            obj.status = UserChallenge.STATUS_PARTIAL
            obj.is_correct = False
            obj.obtained_points = obj.challenge.points // 2  # 50% dos pontos
            obj.evaluated_at = timezone.now()
            obj.save()
        self.message_user(request, f"{queryset.count()} submissões marcadas como parcialmente corretas")
    mark_as_partial.short_description = "Marcar como parcialmente correto"

    def save_model(self, request, obj, form, change):
        if obj.status == UserChallenge.STATUS_CORRECT and not obj.is_correct:
            obj.is_correct = True
            obj.obtained_points = obj.challenge.points
            obj.points_awarded = True
            obj.evaluated_at = timezone.now()
            
            # Atualiza pontos do usuário
            obj.user.points += obj.challenge.points
            obj.user.save()
            
            # Atualiza progresso na trilha
            self.update_track_progress(obj.user, obj.challenge.track)
        
        super().save_model(request, obj, form, change)
    
    def update_track_progress(self, user, track):
        progress, created = UserTrackProgress.objects.get_or_create(
            user=user,
            track=track
        )
        
        completed_challenges = UserChallenge.objects.filter(
            user=user,
            challenge__track=track,
            is_correct=True
        ).count()
        
        total_challenges = track.challenges.count()
        
        if completed_challenges >= total_challenges:
            progress.is_completed = True
            progress.completed_at = timezone.now()
            progress.save()

@admin.register(UserTrackProgress)
class UserTrackProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'track', 'progress_percentage', 'is_completed', 'completed_at']
    list_filter = ['track', 'is_completed']
    search_fields = ['user__username', 'track__title']
    readonly_fields = ['completed_at']
    list_select_related = ['user', 'track']
    
    def progress_percentage(self, obj):
        total = obj.track.challenges.count()
        completed = obj.completed_challenges.count()
        return f"{completed}/{total} ({completed/total*100:.0f}%)" if total > 0 else "0/0 (0%)"
    progress_percentage.short_description = "Progresso"