from ext import db
from datetime import datetime
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
