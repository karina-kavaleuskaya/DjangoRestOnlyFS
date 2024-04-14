from django.apps import AppConfig


class OnlyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'only_app'

