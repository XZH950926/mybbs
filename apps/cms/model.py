from ext import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
class permissions():
    user_info=1
    banner=2
    posts=4
    pinglun=8
    bankuai=16
    user_manager=32

role_user=db.Table(
    "role_user",
    db.Model.metadata,
    db.Column("rid",db.Integer,db.ForeignKey("role.id")),
    db.Column("uid",db.Integer,db.ForeignKey("user.id"))
)
class role(db.Model):
    __tablename__="role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name=db.Column(db.String(20))
    desc=db.Column(db.String(200))
    permis=db.Column(db.Integer,nullable=False,default=permissions.user_info)



class User(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(20),nullable=False)
    _password=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(20),nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)
    roles=db.relationship("role", backref=db.backref("users"), secondary=role_user)

    @property
    def getPermission(self):
        num=0
        for role in self.roles:
            num=num | role.permis
        return num

    def checkPermision(self,permis):
        if self.getPermission & permis !=0:
            return True
        else:
            return False


    def __init__(self,password,**kwargs):
        self.password=password
        kwargs.pop("password",None)
        super(User,self).__init__(**kwargs)

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,frontpwd):
        self._password=generate_password_hash(frontpwd)

    def checkPwd(self,frontpwd):
        return check_password_hash(self._password,frontpwd)


