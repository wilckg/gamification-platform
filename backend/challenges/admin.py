from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Track, Challenge, Question, Option, UserChallenge, UserTrackProgress

# Função auxiliar para desregistrar modelos com segurança
def safe_unregister(model):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

# Desregistra todos os modelos do app challenges (se já estiverem registrados)
safe_unregister(Track)
safe_unregister(Challenge)
safe_unregister(Question)
safe_unregister(Option)
safe_unregister(UserChallenge)
safe_unregister(UserTrackProgress)

# ======================================================
# CLASSES INLINE
# ======================================================
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

# ======================================================
# MODEL ADMIN CLASSES
# ======================================================
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
    list_display = ['user', 'challenge', 'status', 'is_correct', 'obtained_points', 'submitted_at', 'evaluated_at']
    list_filter = ['status', 'is_correct', 'challenge__track', 'challenge__difficulty']
    readonly_fields = ['submitted_at', 'evaluated_at']
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
            'fields': ('submitted_at', 'evaluated_at'),
            'classes': ('collapse',)
        }),
    )

    def mark_as_correct(self, request, queryset):
        for obj in queryset:
            obj.status = 'CORRECT'
            obj.is_correct = True
            obj.obtained_points = obj.challenge.points
            obj.evaluated_at = timezone.now()
            obj.save()
            
            obj.user.points += obj.challenge.points
            obj.user.save()
            
            self.update_track_progress(obj.user, obj.challenge.track)
        
        self.message_user(request, f"{queryset.count()} submissões marcadas como corretas")
    mark_as_correct.short_description = "Marcar como correto"

    def mark_as_incorrect(self, request, queryset):
        updated = queryset.update(
            status='INCORRECT',
            is_correct=False,
            obtained_points=0,
            evaluated_at=timezone.now()
        )
        self.message_user(request, f"{updated} submissões marcadas como incorretas")
    mark_as_incorrect.short_description = "Marcar como incorreto"

    def mark_as_partial(self, request, queryset):
        for obj in queryset:
            obj.status = 'PARTIAL'
            obj.is_correct = False
            obj.obtained_points = obj.challenge.points // 2
            obj.evaluated_at = timezone.now()
            obj.save()
        self.message_user(request, f"{queryset.count()} submissões marcadas como parcialmente corretas")
    mark_as_partial.short_description = "Marcar como parcialmente correto"

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

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

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

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# ======================================================
# ORDENAÇÃO PERSONALIZADA DO MENU ADMIN
# ======================================================

# Salvamos a implementação original
original_get_app_list = admin.AdminSite.get_app_list

def custom_get_app_list(self, request, app_label=None):
    # Chamamos a implementação original
    app_list = original_get_app_list(self, request, app_label)
    
    # Definimos a ordem desejada dos modelos
    model_order = {
        'Track': 1,
        'Challenge': 2,
        'Question': 3,
        'Option': 4,
        'UserChallenge': 5,
        'UserTrackProgress': 6,
    }
    
    # Aplicamos a ordenação apenas para o app 'challenges'
    for app in app_list:
        if app['app_label'] == 'challenges':
            app['models'].sort(key=lambda x: model_order.get(x['object_name'], 999))
    
    return app_list

# Substituímos a implementação original
admin.AdminSite.get_app_list = custom_get_app_list

# Configurações do Admin
admin.site.site_header = "Administração do Sistema"
admin.site.site_title = "Painel de Controle"
admin.site.index_title = "Bem-vindo ao Painel de Administração"