from django.apps import AppConfig
from . import views

class ServerConfig(AppConfig):
    name = 'server'

    def ready(self):
        views.del_ssh_keys()
