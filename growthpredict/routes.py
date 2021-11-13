from growthpredict import app, db, bcrypt
from flask import json,jsonify, render_template,url_for, flash, redirect, request,abort, session,Response
from flask_login import login_user, current_user, logout_user,login_required
#from growthpredict.instagramapi import *
from functools import wraps
from growthpredict.twitterapi import *
from growthpredict.models import *
import os

from growthpredict.forms import *
@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    return render_template('home.html')



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form =RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)

        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created. You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register',form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect (next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()

        if bcrypt.check_password_hash(current_user.password, form.passwordcheck.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            current_user.username = form.username.data
            current_user.email = form.email.data
            user.password = hashed_password
            db.session.commit()
            flash('Success. You change your account', 'success')
        else:
            flash('Unsuccess. Please check correct of yuor input data', 'danger')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title = 'Account', form = form)


@app.route("/add_topic", methods=['GET', 'POST'])
@login_required
def add_topic():
    form = AddTopic()
    if form.validate_on_submit():
        if form.image_file.data:
            file = request.files['image_file'].read()
            nameee = request.files['image_file'].filename
        type = form.type.data
        print(type)
        list_usernames = []
        test2 = file.decode('utf-8')
        separated_string = test2.splitlines()
        print(separated_string)
        list_users = []


        if type == 'Instagram':
            test_topic = Topic_inst(name=form.title.data)
            for elem in separated_string:
                usernam = Post_inst(username=elem)
                db.session.add(usernam)
                test_topic.usernames.append(usernam)
            print(list_users)
            db.session.add(test_topic)
            db.session.commit()

        if type == 'Twitter':
            test_topic2 = Topic_twit(name=form.title.data)
            for elem in separated_string:
                usernam = Post_twit(username=elem)
                db.session.add(usernam)
                test_topic2.usernames.append(usernam)
            print(list_users)
            db.session.add(test_topic2)
            db.session.commit()

        #split_n_0 = read_from_file(file)
        #print(split_n_0)
        #write_csv_medias_info_all(separated_string, "split_n_11.csv")
        #db.session.add()
        #return_parsing_info_all(separated_string)

        #post = Topic(title = form.title.data, content = form.content.data, \
        #            author= current_user, date_posted = date_posted2, \
        #            image_file = file_path_3, tags = form.tags.data, \
        #            already_posted=False,notes= form.notes.data
        #            )
        #db.session.add(post)
        #db.session.commit()
        flash('Your topic has been created!', 'success')
        #return redirect(url_for('home'))
    return render_template('add_topic.html', title='New Topic', form = form, legend = 'New Topic')


def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            return abort(403)
        return func(*args, **kwargs)
    return decorated_view

@app.route('/admin')
@login_required
@admin_login_required
def home_admin():
    if current_user.is_authenticated and current_user.is_admin():
        return render_template('index_admin.html')
    else:
        return render_template('home.html')

