from circle_4.settings.base import *

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
        'NAME': 'world_check',
        'USER': 'trlabs',
        'PASSWORD': '48I44oLmkXS8GXgu',
        'HOST': 'trlabs1.c0sx4azlfegv.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}


MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
)

ALLOWED_HOSTS += ['ec2-52-207-238-213.compute-1.amazonaws.com', 'carbon.amers2.cis.trcloud']


STATIC_URL = '/static/'
STATIC_ROOT = '/home/dreed/static/wc_pep_taxonomy/'
STATICFILES_DIRS = ( '/home/dreed/static/media/', )
