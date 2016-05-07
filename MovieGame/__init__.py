import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging



# instance_relative_config loads specified config file form instance directory
app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py')
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

db = SQLAlchemy(app)
import MovieGame.views
import MovieGame.models
