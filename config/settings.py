
import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


DEBUG = env_bool('KEJACONNECT_DEBUG', default=True)
SECRET_KEY = os.environ.get('KEJACONNECT_SECRET_KEY')
if DEBUG and not SECRET_KEY:
    SECRET_KEY = 'insecure-local-development-key-change-before-deploying'

allowed_hosts_setting = os.environ.get(
    'KEJACONNECT_ALLOWED_HOSTS',
    'localhost,127.0.0.1' if DEBUG else '',
)
ALLOWED_HOSTS = [
    host.strip()
    for host in allowed_hosts_setting.split(',')
    if host.strip()
]
render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_hostname and render_hostname not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_hostname)
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('KEJACONNECT_CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]
if render_hostname:
    render_origin = f'https://{render_hostname}'
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'accounts',
    'locations',
    'listings',
    'interactions',
    'moderation',

    'rest_framework',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if not DEBUG:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

database_url = os.environ.get('DATABASE_URL')
if database_url:
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=not DEBUG,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('KEJACONNECT_DB_NAME', 'keja_connect_db'),
            'USER': os.environ.get('KEJACONNECT_DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('KEJACONNECT_DB_PASSWORD'),
            'HOST': os.environ.get('KEJACONNECT_DB_HOST', 'localhost'),
            'PORT': os.environ.get('KEJACONNECT_DB_PORT', '5432'),
            'CONN_MAX_AGE': 60,
        }
    }

MEDIA_URL = os.environ.get('KEJACONNECT_MEDIA_URL', '/media/')
MEDIA_ROOT = Path(os.environ.get('KEJACONNECT_MEDIA_ROOT', str(BASE_DIR)))
CLOUDINARY_MEDIA_ENABLED = bool(os.environ.get('CLOUDINARY_URL'))

if not DEBUG:
    if not SECRET_KEY:
        raise ImproperlyConfigured('Set KEJACONNECT_SECRET_KEY for production.')
    if not ALLOWED_HOSTS:
        raise ImproperlyConfigured('Set KEJACONNECT_ALLOWED_HOSTS for production.')
    if not DATABASES['default'].get('PASSWORD'):
        raise ImproperlyConfigured('Set DATABASE_URL or KEJACONNECT_DB_PASSWORD for production.')
    if not DATABASES['default'].get('HOST') or DATABASES['default']['HOST'] == 'localhost':
        raise ImproperlyConfigured('Set DATABASE_URL or KEJACONNECT_DB_HOST for production.')
    if not CLOUDINARY_MEDIA_ENABLED and not os.environ.get('KEJACONNECT_MEDIA_ROOT'):
        raise ImproperlyConfigured(
            'Set CLOUDINARY_URL or KEJACONNECT_MEDIA_ROOT for persistent property photo storage.'
        )

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
if not DEBUG:
    STORAGES = {
        'default': {
            'BACKEND': (
                'config.storage.CloudinaryMediaStorage'
                if CLOUDINARY_MEDIA_ENABLED
                else 'django.core.files.storage.FileSystemStorage'
            ),
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:dashboard'
LOGOUT_REDIRECT_URL = '/'

SECURE_SSL_REDIRECT = env_bool('KEJACONNECT_HTTPS', default=not DEBUG)
SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') if not DEBUG else None
SECURE_HSTS_SECONDS = int(os.environ.get('KEJACONNECT_HSTS_SECONDS', '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool(
    'KEJACONNECT_HSTS_INCLUDE_SUBDOMAINS', default=False
)
SECURE_HSTS_PRELOAD = env_bool('KEJACONNECT_HSTS_PRELOAD', default=False)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'same-origin'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}
