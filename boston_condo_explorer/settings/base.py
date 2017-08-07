import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIVATE_DIR = os.path.join(BASE_DIR, 'private')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vwr5#e79cpb&&tax3qkpy6!9fk^&3m1bx+lk2#j2e&3twmk$!='

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'base',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_extensions',
    'django_filters',

    'rest_framework_swagger',
)

ROOT_URLCONF = 'boston_condo_explorer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

WSGI_APPLICATION = 'boston_condo_explorer.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static/')

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'boston_condo_explorer.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 50,  # Default to 10
    'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 2000,  # Maximum limit allowed when using `?page_size=xxx`.
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}

INTERNAL_IPS = [
    '127.0.0.1'
]

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
}

LOGIN_URL = 'auth:login'
LOGOUT_URL = 'auth:logout'

EMAIL_HOST = 'smtp.pln.corp.services'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'noreply@tr.com'
DEFAULT_FROM_EMAIL = 'noreply@tr.com'

CELERY_IMPORTS = ('base.tasks',)

CELERYBEAT_SCHEDULE = {
    'run-all': {
        'task': 'base.tasks.scrape_all_listings_task',
        'schedule': 20.0
    }
}

# Custom Settings
def get_key(fname):
    with open(fname, 'r') as f:
        first_line = f.readline()

    return first_line.strip()

GOOGLE_KEY = get_key(os.path.join(PRIVATE_DIR, 'google.key'))
AID_KEY = get_key(os.path.join(PRIVATE_DIR, 'aid.key'))

MLS_URLS = {
    'results_url': 'http://vow.mlspin.com/idx/rslts.aspx',
    'details_url': 'http://vow.mlspin.com/idx/details.aspx'
}

QUERY = {
  "towns": ["BOST", "CAMB"],
  "types": ["SF", "CC"],
  "price": [600000, 900000],
  "beds": 1,
  "baths": 1
}
