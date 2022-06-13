import os
from src.settings.local import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'MozioInterview',
#         'USER': 'postgres',
#         'PASSWORD': 'letmein20116199623',
#         'HOST': 'localhost',
#         'PORT': 5432
#     }
# }

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
