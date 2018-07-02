import pymysql

pymysql.install_as_MySQLdb()

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

INSTALLED_APPS += ('mysql_app',)

