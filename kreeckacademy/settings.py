
from django.conf import settings
import os
import posixpath
import environ
from decouple import config

# Environment variables
env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

USE_X_FORWARDED_HOST = True

# Allow the Debug Toolbar to appear for all IP addresses (only use this in development)
INTERNAL_IPS = [
    '127.0.0.1',
]

if DEBUG:
    ALLOWED_HOSTS = [
        '*',
        'localhost',
        '127.0.0.1',
        'compiler',
        'kreeckacademy.s3.amazonaws.com',
        'http://django-env.eba-gmw2zn2q.ap-south-1.elasticbeanstalk.com/',
    ]
else:
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
# change the default user models to our custom model
AUTH_USER_MODEL = 'accounts.User' 

# Application definition
CSRF_TRUSTED_ORIGINS = [
    "https://academykreeck.azurewebsites.net",
    "https://kreeck.com",
    "http://kreeck.com",
    "http://academykreeck.azurewebsites.net",
    'http://academy.kreeck.com',
    'https://academy.kreeck.com',
    'https://kreeckacadeny.azurewebsites.net',
    'http://kreeckacadeny.azurewebsites.net'
]
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup',
]

""" Adding cross domain authentication the initial functionality of this is to have a centralized authentication application that is deployed on 
    www.auth.kreeck.com, this will allow all the users to have one profile for all the kreeck applications
"""
THIRED_PARTY_APPS = [
    
    'rest_framework',
    'debug_toolbar',
    'crispy_forms',
    "crispy_bootstrap4",
    'tinymce',

    #tailwind configurations
    'tailwind',
    'theme',
    #'django_browser_reload',

    ############
    'corsheaders' # This will handle the central login application that is yet to be implemented, as of yet i want to set the functionalities
]


NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"
 
# Custom apps
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
    #'support', Enable this support functionality when you are in production only
    'compiler',
    'common',
    'student_record',
    
]


# Combine all apps
INSTALLED_APPS = DJANGO_APPS + THIRED_PARTY_APPS + PROJECT_APPS

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
    #'support.middleware.ErrorLoggingMiddleware', Enable this only when in Production
    'app.middleware.RedirectMiddleware',
    #"django_browser_reload.middleware.BrowserReloadMiddleware",
]


ROOT_URLCONF = 'kreeckacademy.urls'

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
                
                # 'django.template.context_processors.i18n',
                # 'django.template.context_processors.media',
                # 'django.template.context_processors.static',
                # 'django.template.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'kreeckacademy.wsgi.application'

ASGI_APPLICATION = "kreeckacademy.asgi.application"


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,  # Set this to True to intercept redirects for debugging
    'SHOW_TOOLBAR_CALLBACK': lambda request: settings.DEBUG,
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if DEBUG:
#the local db is the sql lite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

#If the code is in Production use the Postgresql DB
else: 
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



"""The Kreeck central authentication will handle the remote authentication once the external authentication application is set us"""
KREECK_CENTRAL_AUTH = False
if KREECK_CENTRAL_AUTH:
    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.RemoteUserBackend',
    ]
else:
    pass


TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "code,help,wordcount"
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True




# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True





# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = True  # Enable query string authentication

#If debug is True it must use the local file storage to access the web app files and static files
if DEBUG:
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
    STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['staticfiles']))
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')


else:
    STATIC_URL = 'https://d2bzxomyx8oypj.cloudfront.net/static/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # Use 'storages' backend for media files to utilize AWS S3
    # Manages the bucket objects with cloudfront
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = 'https://d2bzxomyx8oypj.cloudfront.net/'

    

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_SSL = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')


# crispy config
CRISPY_TEMPLATE_PACK = 'bootstrap4'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = '/auth/login/'

# DRF setup
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'common.authentication.APIKeyAuthentication', 
    ],
    #NOTE : Only enable this in production
    #'EXCEPTION_HANDLER': 'support.exception_handler.custom_exception_handler',
}

TAILWIND_APP_NAME = 'theme'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Strip payment config
# STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
# STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')

# Add Stripe configuration
STRIPE_LIVE_PUBLISHABLE_KEY = config('STRIPE_LIVE_PUBLISHABLE_KEY')
STRIPE_LIVE_SECRET_KEY = config('STRIPE_LIVE_SECRET_KEY')
STRIPE_TEST_SECRET_KEY = config('STRIPE_TEST_SECRET_KEY')
STRIPE_TEST_PUBLISHABLE_KEY = config('STRIPE_TEST_PUBLISHABLE_KEY')
STRIPE_LIVE_MODE = False  # Change to True in production
