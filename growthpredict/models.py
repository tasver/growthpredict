from datetime import datetime
from growthpredict import db, login_manager
from flask_login import UserMixin
from hashlib import md5
from flask import Flask, request, jsonify, make_response
import uuid

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    admin = db.Column(db.Boolean())

    def __repr__(self):
        return self.username

    def __init__(self, username, email, password, admin=True):
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin

    def is_admin(self):
        return self.admin

class Post_inst(db.Model):
    __tablename__ = 'posts_inst'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    avg_views = db.Column(db.Float)
    avg_likes = db.Column(db.Float)
    avg_comments = db.Column(db.Float)
    followers = db.Column(db.Integer)
    media = db.Column(db.Integer)
    avg_er = db.Column(db.Float)
    growth = db.Column(db.Float)
    growth_predict = db.Column(db.Float)
    def __repr__(self):
        return self.username

class Post_twit(db.Model):
    __tablename__ = 'posts_twit'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    avg_view_count = db.Column(db.Float)
    avg_retweet_count = db.Column(db.Float)
    avg_reply_count = db.Column(db.Float)
    avg_like_count = db.Column(db.Float)
    avg_quote_count = db.Column(db.Float)
    media = db.Column(db.Integer)
    avg_er = db.Column(db.Float)
    growth = db.Column(db.Float)
    growth_predict = db.Column(db.Float)
    followers = db.Column(db.Integer)
    def __repr__(self):
        return self.username

class Topic_inst(db.Model):
    __tablename__ = 'topics_inst'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    model_linear = db.Column(db.PickleType())
    model_poly = db.Column(db.PickleType())
    poly = db.Column(db.PickleType())
    usernames = db.relationship('Post_inst', secondary='topic_posts_inst')

class TopicPosts_inst(db.Model):
    __tablename__ = 'topic_posts_inst'
    id = db.Column(db.Integer(), primary_key=True)
    topic_id = db.Column(db.Integer(), db.ForeignKey('topics_inst.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts_inst.id', ondelete='CASCADE'))

class Topic_twit(db.Model):
    __tablename__ = 'topics_twit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    model_linear = db.Column(db.PickleType())
    model_poly = db.Column(db.PickleType())
    poly= db.Column(db.PickleType())
    usernames = db.relationship('Post_twit', secondary='topic_posts_twit')

class TopicPosts_twit(db.Model):
    __tablename__ = 'topic_posts_twit'
    id = db.Column(db.Integer(), primary_key=True)
    topic_id = db.Column(db.Integer(), db.ForeignKey('topics_twit.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts_twit.id', ondelete='CASCADE'))


def init_db():
    #models.Post_twit.query.delete()
    db.create_all()

    # Create a test user
    #new_user = User('a@a.com', 'aaaaaaaa')
    #new_user.display_name = 'Nathan'
    #db.session.add(new_user)
    #db.session.commit()

    new_task_t = Post_twit(username='test')
    db.session.add(new_task_t)
    db.session.commit()
    new_task_i = Post_inst(username='test')
    db.session.add(new_task_i)
    db.session.commit()
    new_topic_i = Topic_inst(name='test')
    db.session.add(new_topic_i)
    db.session.commit()
    new_topic_t = Topic_twit(name='test')
    db.session.add(new_topic_t)
    db.session.commit()
    #new_user.datetime_subscription_valid_until = datetime.datetime(2019, 1, 1)
    db.session.commit()

if __name__ == '__main__':
    init_db()
