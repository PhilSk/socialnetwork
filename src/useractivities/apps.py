from __future__ import unicode_literals

from django.apps import AppConfig


class UseractivitiesConfig(AppConfig):
    name = 'useractivities'

    def ready(self):
        import signals
        signals.init_signals()