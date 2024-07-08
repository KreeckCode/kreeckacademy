from .settings import *

DEBUG = False

ALLOWED_HOSTS = [
    '*',
    'localhost',
    '127.0.0.1',
    'compiler',
    'http://django-env.eba-gmw2zn2q.ap-south-1.elasticbeanstalk.com/',
    'kreeckacademy.s3.amazonaws.com',
    'https://academykreeck.azurewebsites.net',
    'http://kreeckacadeny.azurewebsites.net',
    'https://academy.kreeck.com',
    'http://academy.kreeck.com',
    'https://kreeck.com',
    'http://kreeck.com'
]

# Database settings for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# Email settings for production
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_SSL = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# Static and media files settings for production with AWS S3
STATIC_URL = 'https://d2bzxomyx8oypj.cloudfront.net/static/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = 'https://d2bzxomyx8oypj.cloudfront.net/'
