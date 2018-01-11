from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysql',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'mariadb',
        'PORT': 3306,
    },
}

INSTALL_APPS += ('mysql_app',)

