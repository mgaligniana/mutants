import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(app.config.from_object(os.environ["APP_SETTINGS"]))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from . import api

app.register_blueprint(api.bp)

from .models import DNA
