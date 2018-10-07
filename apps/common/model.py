from ext import db
from datetime import datetime
from apps.front.model import Front_USER
import shortuuid
class Banner(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    bannerName = db.Column(db.String(20),nullable=False)
    imglink = db.Column(db.String(200),nullable=False,unique=True)
    link = db.Column(db.String(200),nullable=False,unique=True)
    priority = db.Column(db.Integer,default=1)

class Border(db.Model):
    __tablename__ = 'border'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    borderName = db.Column(db.String(20),nullable=False)
    postNum=db.Column(db.Integer,nullable=False,default=0)
    create_time=db.Column(db.String(40),default=datetime.now)

class Post(db.Model):
    __tablename__="post"
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    title=db.Column(db.String(40),nullable=False)
    user=db.relationship("Front_USER",backref="posts")
    user_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))
    border=db.relationship("Border",backref="posts")
    border_id = db.Column(db.Integer, db.ForeignKey("border.id"))
    content=db.Column(db.Text)
    views=db.Column(db.Integer,default=0)
    create_time=db.Column(db.DateTime,default=datetime.now)

class Common(db.Model):
    __tablename__ = "common"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    post = db.relationship('Post',backref='commons')
    user_id = db.Column(db.String(100), db.ForeignKey('front_user.id'), default=shortuuid.uuid)
    user = db.relationship('Front_USER', backref='commons')  # orm查询的时候使用
    create_time = db.Column(db.DateTime, default=datetime.now)


class Tag(db.Model):
    __tablename__="tag"
    id =db.Column(db.Integer,primary_key=True,autoincrement=True)
    post_id=db.Column(db.Integer,db.ForeignKey("post.id"))
    isTag=db.Column(db.Boolean,default=False)
    post = db.relationship('Post', backref=db.backref('tag', uselist=False))
    create_time = db.Column(db.DateTime, default=datetime.now)