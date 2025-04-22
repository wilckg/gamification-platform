from django.apps import AppConfig

class ChallengesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "challenges"
    
    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.ready_run = False
    
    def ready(self):
        if not self.ready_run:
            # Importa os signals apenas depois que o app estiver pronto
            try:
                from . import signals
                self.ready_run = True
            except ImportError:
                self.ready_run = False