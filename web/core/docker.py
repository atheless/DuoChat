from web.core.settings.base import *

from os import environ

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ['POSTGRES_DB'],
        'USER': environ['POSTGRES_USER'],
        'PASSWORD': environ['POSTGRES_PASSWORD'],
        'HOST': environ['POSTGRES_SERVICE'],
        'PORT': environ['POSTGRES_PORT'],
    }
}
