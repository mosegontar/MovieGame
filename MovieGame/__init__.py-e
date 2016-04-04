import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# instance_relative_config loads specified config file form instance directory
app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py')


db = SQLAlchemy(app)

import MovieGame.views
import MovieGame.models
