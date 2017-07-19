import sys
from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL']
        )

    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery



app = Flask(__name__)

app.config.from_object('mls_scraper.settings')
app.config['PKG_NAME'] = __name__

celery = make_celery(app)
db = SQLAlchemy(app)


logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s][%(levelname)s] :: %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
