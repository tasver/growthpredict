from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#from settings import *
from flask_admin import Admin, BaseView, expose

app = Flask(__name__)

config_file='settings.py'
app.config.from_pyfile(config_file)

db = SQLAlchemy(app)
migrate = Migrate(app,db)



bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flask_admin.contrib.sqla import ModelView
import growthpredict.forms as views
admin = Admin(app, template_mode='bootstrap3',index_view=views.MyAdminIndexView())
admin.add_view(ModelView(views.User, db.session))
admin.add_view(ModelView(views.Post_inst, db.session))
admin.add_view(ModelView(views.Post_twit, db.session))
admin.add_view(ModelView(views.Topic_inst, db.session))
admin.add_view(ModelView(views.Topic_twit, db.session))

from growthpredict import routes, models