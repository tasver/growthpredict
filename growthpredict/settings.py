import os
from os import environ
from sqlalchemy import create_engine
#SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = os.urandom(32)
#app.config['SECRET_KEY'] = SECRET_KEY

basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
import os
import re

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
#db_uri = environ.get('SQLALCHEMY_DATABASE_URI')
engine = create_engine(uri, echo=True)