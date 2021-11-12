from growthpredict import app, db, bcrypt
from flask import json,jsonify, render_template,url_for, flash, redirect, request,abort, session,Response
from flask_login import login_user, current_user, logout_user,login_required
from growthpredict.instagramapi import *
from growthpredict.twitterapi import *
from growthpredict.models import *
import os
from growthpredict.forms import *
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World! Tolik LOH"

@app.route('/home')
def home():
    user = {'username': 'Miguel'}
    return render_template('home.html', title='Home', user=user)

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
        list_usernames = []
        print(file)

        #for line in file:
        #    current_username = line[:-1]
        #    list_usernames.append(current_username)
        #print(list_usernames)
        #split_n_0 = read_from_file(file)
        #print(split_n_0)
        #write_csv_medias_info_all(split_n_0, "split_n_11.csv")

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