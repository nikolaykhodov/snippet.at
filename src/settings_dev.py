# -*- coding: utf-8 -*-
# !!! ОТЛАДОЧНЫЕ НАСТРОЙКИ !!!!!

import os
p = lambda dir: os.path.join(os.path.dirname(__file__), dir)
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': p('snippet.sqlite'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'info@google.ru'

# Путь к директории с верстаемыми шаблонами
DEBUGPAGES_TEMPLATE_DIR = p('templates/new')

# Префикс URL для стастики, используемой в верстаемых шаблонах
DEBUGPAGES_STATIC_URL = '/static/new/'

# Путь к директории со статикой верстаемых страниц
DEBUGPAGES_STATICFILE_DIR = p('static/new')

import logging
logging.basicConfig(level=logging.DEBUG)
