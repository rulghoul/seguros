from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY","emqctex@x=j1z&bcdlz67vj3_db($ks9(49c0y=p(#uwllb28l")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG","1")


#ALLOWED_HOSTS = ["*"]
ALLOWED_HOSTS = os.getenv('SEGUROS_ALLOWED_HOSTS', 'localhost,seguros-django.ifnap8.easypanel.host').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('SEGUROS_CSRF_TRUSTED_ORIGINS', 'https://seguros.ghoulrul.online,http://localhost,https://seguros-django.ifnap8.easypanel.host').split(',')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Application definition

INSTALLED_APPS = [
    "tema",
    "documentos",
    "sepomex",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_bootstrap5",
    'crispy_forms',
    "crispy_bootstrap5",   
    'simple_history',
    'fontawesomefree',
    'colorfield',
    'django_ckeditor_5',
    'django_select2',
    'django_tables2',
    'django_filters',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = "seguros.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "documentos.context_processors.asesor_status", #Valida si el usuario si es 
            ],
        },
    },
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'
SELECT2_BOOTSTRAP = True
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap5-responsive.html"
MAXIMOS_ADICIONALES = 5
WSGI_APPLICATION = "seguros.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": os.environ.get("SEGUROS_SQL_ENGINE",  "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SEGUROS_SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SEGUROS_SQL_USER", "user"),
        "PASSWORD": os.environ.get("SEGUROS_SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SEGUROS_SQL_HOST", "localhost"),
        "PORT": os.environ.get("SEGUROS_SQL_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("SEGUROS_REDIS", "redis://default:a10a03eb865b16a0d018@seguros_redis:6379") + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("SEGUROS_REDIS", "redis://default:a10a03eb865b16a0d018@seguros_redis:6379") + "/2",        
        "TIMEOUT": 60 * 60 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "select2"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "es-mx"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

#STATIC_URL = "static/"

#STATIC_URL = "static/"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static') 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

CKEDITOR_BASEPATH =  os.path.join(STATIC_ROOT,"ckeditor/ckeditor/")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#gmail_send/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'valor_por_defecto')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'valor_por_defecto')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'elmonjeamarillo@gmail.com'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

#Parametros de archivos
MAX_FILE_SIZE_MB = os.environ.get('MAX_FILE_SIZE_MB', 1)
ENCRYPTION_KEY = b'_DVWRoqmwRLj-ywo5h0eD0QqaQJeL2ZzQ5hPqQMwX3U='
ALLOWED_FILE_TYPES = os.environ.get('ALLOWED_FILE_TYPES','application/pdf,image/jpeg,image/png,image/webp').split(',')