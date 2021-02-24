from django.apps import AppConfig


class PizzalabappConfig(AppConfig):
    name = 'pizzalabapp'

    def ready(self):
        import pizzalabapp.signals
