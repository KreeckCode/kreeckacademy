import os
from decouple import config
from django.conf import settings
from decouple import config
import os
import posixpath
import environ

# Environment variables
env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SSL certificates path
SSL_CERTIFICATE_DIR = os.path.join(BASE_DIR, 'SECURITY_CERTIFICATES', 'kreeck_com')

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

USE_X_FORWARDED_HOST = True

INTERNAL_IPS = [
    '127.0.0.1',
]

ALLOWED_HOSTS = [
    '*',
    'localhost',
    '127.0.0.1',
    'compiler',
    'kreeckacademy.s3.amazonaws.com',
    'http://django-env.eba-gmw2zn2q.ap-south-1.elasticbeanstalk.com/',
]

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'debug_toolbar',
    'crispy_forms',
    'crispy_bootstrap4',
    'tinymce',
    'corsheaders',
]

PROJECT_APPS = [
    'app.apps.AppConfig',
    'accounts.apps.AccountsConfig',
    'course.apps.CourseConfig',
    'result.apps.ResultConfig',
    'search.apps.SearchConfig',
    'quiz.apps.QuizConfig',
    'blog.apps.BlogConfig',
    'hackathon',
    'payments',
    'support',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'support.middleware.ErrorLoggingMiddleware',
]

ROOT_URLCONF = 'SMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SMS.wsgi.application'

ASGI_APPLICATION = "SMS.asgi.application"

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': lambda request: settings.DEBUG,
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static files settings
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
