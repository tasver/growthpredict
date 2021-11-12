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

    admin = db.Column(db.Boolean(True))

    def __repr__(self):
        return self.username

    def __init__(self, username, email, password, admin=False):
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
    pk = db.Column(db.String(120))
    id_post = db.Column(db.String(120))
    code = db.Column(db.String(120))
    link = db.Column(db.String(120))
    views = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    followers =db.Column(db.Integer)
    def __repr__(self):
        return self.username

class Post_twit(db.Model):
    __tablename__ = 'posts_twit'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    author_id = db.Column(db.String(120))
    tweet_id = db.Column(db.String(120))
    tweet_link = db.Column(db.String(120))
    view_count = db.Column(db.Integer)
    retweet_count = db.Column(db.Integer)
    reply_count = db.Column(db.Integer)
    like_count = db.Column(db.Integer)
    quote_count = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    def __repr__(self):
        return self.username

class Topic_inst(db.Model):
    __tablename__ = 'topics_inst'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    avg_views = db.Column(db.Integer)
    avg_likes = db.Column(db.Integer)
    avg_comments = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    media = db.Column(db.Integer)
    avg_er = db.Column(db.Integer)
    growth = db.Column(db.Integer)
    growth_predict = db.Column(db.Integer)
    posts = db.relationship('Post_inst', secondary='topic_posts_inst')

class TopicPosts_inst(db.Model):
    __tablename__ = 'topic_posts_inst'
    id = db.Column(db.Integer(), primary_key=True)
    topic_id = db.Column(db.Integer(), db.ForeignKey('topics_inst.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts_inst.id', ondelete='CASCADE'))

class Topic_twit(db.Model):
    __tablename__ = 'topics_twit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    avg_view_count = db.Column(db.Integer)
    avg_retweet_count = db.Column(db.Integer)
    avg_reply_count = db.Column(db.Integer)
    avg_like_count = db.Column(db.Integer)
    avg_quote_count = db.Column(db.Integer)
    media = db.Column(db.Integer)
    avg_er = db.Column(db.Integer)
    growth  = db.Column(db.Integer)
    growth_predict = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    posts = db.relationship('Post_twit', secondary='topic_posts_twit')

class TopicPosts_twit(db.Model):
    __tablename__ = 'topic_posts_twit'
    id = db.Column(db.Integer(), primary_key=True)
    topic_id = db.Column(db.Integer(), db.ForeignKey('topics_twit.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts_twit.id', ondelete='CASCADE'))



