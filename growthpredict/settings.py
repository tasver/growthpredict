import os
from os import environ
from sqlalchemy import create_engine
#SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = os.urandom(32)
#app.config['SECRET_KEY'] = SECRET_KEY

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://mmmdasrcynxnoc:c84c95ae88cd24be00ea751da1e92f82b1e3418022929966def6a054340ae8e4@ec2-3-230-149-158.compute-1.amazonaws.com:5433/d4gfugsi3nv9a'
SQLALCHEMY_TRACK_MODIFICATIONS = False
import os
import re

#uri = os.getenv("DATABASE_URL")  # or other relevant config var
#if uri and uri.startswith("postgres://"):
#    uri = uri.replace("postgres://", "postgresql://", 1)
#db_uri = environ.get('SQLALCHEMY_DATABASE_URI')
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)