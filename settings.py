import os
from utils import *
import logging

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PRIVATE_DIR = os.path.join(BASE_DIR, 'private')

GOOGLE_KEY = get_key(os.path.join(PRIVATE_DIR, 'google.key'))
AID_KEY = get_key(os.path.join(PRIVATE_DIR, 'aid.key'))
BASE_URL = 'http://vow.mlspin.com/idx/rslts.aspx'

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/mls_listings.db'.format(BASE_DIR)
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_DATABASE_URI = 'postgresql://dreed@blue.amers2.cis.trcloud:5432/datalab'



# logging_config = dict(
#     version=1,
#     formatters={
#         'f': {'format':
#               '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
#     },
#     handlers={
#         'h': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'f',
#             'level': logging.DEBUG
#         },
#         'console': {
#             'level': 'DEBUG',
#             'formatter': 'f',
#             'class': 'logging.StreamHandler',
#         },
#         'file': {
#             'level': 'DEBUG',
#             'formatter': 'f',
#             'class': 'logging.FileHandler',
#             'filename': '%sdebug.log' % BASE_DIR,
#         }
#     },
#     loggers={
#         'root': {'handlers': ['console', 'file'],
#                  'level': logging.DEBUG}
#     }
# )
#
# dictConfig(logging_config)
#
# logger = logging.getLogger('root')
