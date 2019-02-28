import time
import threading

from django.apps import AppConfig
from django.conf import settings

DEFAULT_DELAYED_SECONDS = 1


class D2aConfig(AppConfig):
    name = 'd2a'

    def ready(self):
        import d2a
        t = threading.Thread(target=d2a.autoload)
        t.start()

        # makes django's loading apps delayed.
        config = getattr(settings, 'D2A_CONFIG', {})
        autoload_config = config.get('AUTOLOAD', {})
        autoload_sleep = autoload_config.get('sleep', DEFAULT_DELAYED_SECONDS)
        time.sleep(autoload_sleep)
