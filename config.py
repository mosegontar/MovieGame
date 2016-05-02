import os
DEBUG = False
SECRET_KEY = os.environ.get('SECRETKEY')
API_KEY = os.environ.get("APIKEY")
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', default="sqlite:///")

