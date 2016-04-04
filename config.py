import os
DEBUG = False
SECRET_KEY = os.environ.get('SECRETKEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', default="sqlite:///")
