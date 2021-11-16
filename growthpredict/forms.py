from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectField, widgets, DateTimeField, StringField, PasswordField, SubmitField, BooleanField,TextAreaField,SelectMultipleField
from wtforms.validators import InputRequired, DataRequired, Length, Email, EqualTo, ValidationError, Optional
from growthpredict.models import *
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import email_validator
from flask import flash, redirect, url_for, Markup
#from wtforms.fields.html5 import DateField
#from wtforms_components import TimeField, TimeRange
#from wtforms.widgets.html5 import TimeInput
#from flask_admin.contrib.sqla import ModelView
#from flask_admin import BaseView, expose, AdminIndexView
#from flask_admin.form import rules
#from autopost import bcrypt
import datetime


class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password',validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators = [DataRequired(), EqualTo('password')])
    submit= SubmitField('Sign up')
    def validate_field(self,field):
        if True:
            raise ValidationError('Validation message')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class LoginForm(FlaskForm):
    email =StringField('Email', validators = [DataRequired(),Email()])
    password = PasswordField('Password',validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit= SubmitField('Log in')

class UpdateAccountForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email', validators=[DataRequired(),Email()])
    submit= SubmitField('Update')
    new_password = PasswordField('New password',validators = [DataRequired()])
    passwordcheck = PasswordField('Old password',validators = [DataRequired()])
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one')
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class AddTopic(FlaskForm):
    title = StringField('Title', validators=[DataRequired()],render_kw={"placeholder": "It is your content title"})
    image_file = FileField('Choose txt file with usernames', validators=[FileAllowed(['txt']),DataRequired()])
    type = SelectField(u'Type', choices=[('Twitter', 'Twitter'), ('Instagram', 'Instagram')])
    submit = SubmitField('Add topic')

#class AddPredict(FlaskForm):
#    username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder": "Enter your username"})
#    topic = StringField('Choose topic', validators=[DataRequired()],render_kw={"placeholder": "Enter your username"})
#    submit = SubmitField('Make predict')

class AddPredict(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],render_kw={"placeholder": "Enter your username"})
    topic = StringField('Choose topic', validators=[DataRequired()],render_kw={"placeholder": "Enter your username"})
    predict_value = StringField('This is predict Value')
    growth_procent = StringField('Predict growth in %')
    max_of_scale = StringField('Max of this scale')
    quality = StringField('Your quality is ')
    submit = SubmitField('Make predict')

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

