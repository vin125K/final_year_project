from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_migrate

class DigicareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DigiCare'

    def ready(self):
        def disconnect_user_logged_in(sender, **kwargs):
            if 'update_last_login' in kwargs:
                update_last_login = kwargs.pop('update_last_login')
                user_logged_in.disconnect(update_last_login)

        post_migrate.connect(disconnect_user_logged_in, sender=self)
