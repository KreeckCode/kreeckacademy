from .settings import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Database settings for development (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Email settings for development (output to console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
