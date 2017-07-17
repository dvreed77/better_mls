from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('settings')
app.config['PKG_NAME'] = __name__

db = SQLAlchemy(app)
