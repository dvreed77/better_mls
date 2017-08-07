from boston_condo_explorer.settings.base import *

DEBUG = True
# CACHE_MIDDLEWARE_ALIAS = 'default'
# CACHE_MIDDLEWARE_SECONDS = 20*60

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': 'carbon.amers2.cis.trcloud:11211',
#         # 'TIMEOUT': None,
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mls',
        'USER': 'dreed',
        'PASSWORD': 'dreed',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
)

ALLOWED_HOSTS += ['www.dvreed.com', 'dvreed.com']


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# STATICFILES_DIRS = ( '/home/dreed/static/media/', )
