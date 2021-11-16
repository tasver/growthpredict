import pandas

from growthpredict import app, db, bcrypt
from flask import json,jsonify, render_template,url_for, flash, redirect, request,abort, session,Response
from flask_login import login_user, current_user, logout_user,login_required
#from growthpredict.instagramapi import *
from functools import wraps
from growthpredict.twitterapi import *
from growthpredict.models import *
import os
from worker import *
import time
from growthpredict.forms import *
from datetime import datetime
import pickle

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



        if type == 'Instagram':
            test_topic = Topic_inst(name=form.title.data)
            for elem in separated_string:
                usernam = Post_inst(username=elem)
                db.session.add(usernam)
                test_topic.usernames.append(usernam)
            print(test_topic)
            db.session.add(test_topic)
            db.session.commit()

        if type == 'Twitter':
            test_topic = Topic_twit(name=form.title.data)
            #for elem in separated_string:
            #    usernam = Post_twit(username=elem)
            #    #db.session.add(usernam)
            #    test_topic.usernames.append(usernam)
            #print(test_topic)
            #db.session.add(test_topic)
            #db.session.commit()
            namefile = test_topic.name + '.csv'
            date_posted = datetime.now() + timedelta(minutes=1)
            write_many(separated_string, f'growthpredict/tmp/{namefile}')
            get_avg_without_media_growth(f'growthpredict/tmp/{namefile}',test_topic)
            placeholder = '?'
            testttt=[]
            placee = test_topic.query.filter_by(name=form.title.data).first()
            print(placee)
            place_users = placee.usernames
            test_str = str(place_users)
            test_str2 = test_str[1:-1]
            test_str3 = test_str2.replace(',',' ').split()
            test_str4 = str(test_str3)[1:-1]
            print(test_str4)


            sql_df = pd.read_sql(
                #'SELECT * FROM posts_twit WHERE username in (%s)' % placeholders,
                #'SELECT * FROM posts_twit WHERE username in {}'.format(tuple_test),
                #'SELECT * FROM posts_twit WHERE username in ("realmadrid")',
                #f'SELECT * FROM posts_twit WHERE username in ({", ".join(separated_string)})',
                #f'SELECT * FROM posts_twit WHERE username = {"realmadrid"}',
                #"SELECT * FROM topics_twit WHERE name in f'{test_topic.name}'",
                f'SELECT * FROM posts_twit WHERE username in ({test_str4})',
                #'SELECT * FROM posts_twit WHERE exists (SELECT name FROM topics_twit WHERE usernames = posts_twit.username)',
                con=engine,

            )
            print(sql_df)
            namefile1='test_twitter_file_for.csv'
            data2, scale, max_of_scale = normalising_data_and_create_scale_from_file(f'growthpredict/tmp/{namefile1}')
            print('data2 is')
            #pandas.set_option('display.max_rows', data2.shape[0] + 1)
            #pandas.set_option('display.max_columns', data2.shape[1] + 1)
            print(data2)
            test_model_poly, test_poly = create_poly2_model_from_bd(data2)
            print(test_model_poly)
            test_linear = create_linear_model_from_bd(data2)
            print(test_linear)

            data_for_save_model_poly = pickle.dumps(test_model_poly)
            data_for_save_poly = pickle.dumps(test_poly)
            data_for_save_model_linear = pickle.dumps(test_linear)
            value = Topic_twit.query.filter(Topic_twit.name == str(form.title.data)).first()
            value.model_linear = data_for_save_model_linear
            value.model_poly = data_for_save_model_poly
            value.poly = data_for_save_poly
            db.session.flush()
            db.session.commit()
            #MlModels.objects.create(model=data)

            value2 = Topic_twit.query.filter(Topic_twit.name == str(form.title.data)).first()
            model_new_poly = pickle.loads(value2.model_poly)
            print("this is first")
            print(data_for_save_model_poly)
            print("this is second")
            print(model_new_poly)
            new_poly = pickle.loads(value2.poly)
            model_new_linear = pickle.loads(value2.model_linear)
            file_for_predict = 'test_1twitter.csv'
            print(use_poly2_model(f'growthpredict/tmp/{file_for_predict}',test_model_poly, test_poly))
            print(use_linear_model(f'growthpredict/tmp/{file_for_predict}', test_linear))

            print("test use withh download models")
            print(use_poly2_model(f'growthpredict/tmp/{file_for_predict}', model_new_poly, new_poly))
            print(use_linear_model(f'growthpredict/tmp/{file_for_predict}', model_new_linear))
            """
            file_for_predict22 = 'TWITTER_TEST_csv.csv'
            print('secondtry')
            test_model_poly2, test_poly2 = create_poly2_model_from_file(f'growthpredict/tmp/{file_for_predict22}')
            print(test_model_poly2)
            test_linear2 = create_linear_model_from_file(f'growthpredict/tmp/{file_for_predict22}')
            print(test_linear2)

            file_for_predict2 = 'test_1twitter.csv'
            print(use_poly2_model(f'growthpredict/tmp/{file_for_predict2}', test_model_poly2, test_poly2))
            print(use_linear_model(f'growthpredict/tmp/{file_for_predict2}', test_linear2))
            """

        #job = queue.enqueue_at(date_posted, write_many,separated_string,'test_file1.csv', result_ttl=-1)
        #registry = ScheduledJobRegistry(queue=queue)
        #print(job in registry)
        #print('Job id: %s' % job.id)
        #if post.job_id == None:
        #    post.job_id = str(job.id)
        #else:
        #    post.job_id = str(post.job_id) + str(job.id)

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

