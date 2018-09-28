from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from apps.common.memcached import getmem
from apps.common.response import *
from apps.cms.model import *
from flask import jsonify
#？
class Error(FlaskForm):
    @property
    def err(self):
        return self.errors.popitem()[1][0]

class checkForm(Error):
    password=StringField(validators=[Length(min=6,max=60,message="密码必须是6-60位"),InputRequired(message="密码不能为空")])
    email=StringField(validators=[Email(message="输入的必须是邮箱"),InputRequired(message="输入的不能为空")])

class resetpwdForm(Error):
    password1=StringField(validators=[Length(min=6,max=60,message="旧密码必须是6-60位"),InputRequired(message="就密码不能为空")])
    password2=StringField(validators=[Length(min=6,max=60,message="新密码必须是6-60位"),InputRequired(message="新密码必须不为空")])
    password3=StringField(validators=[Length(min=6,max=60,message="新密码必须是6-60位"),InputRequired(message="新密码必须不为空"),EqualTo("password2",message="输入的新密码必须一致")])


class resetEmail(Error):
    email=StringField(validators=[Email(message="输入的必须是邮箱")])
    def valide_email(self,filed):
        user = User.query.filter(User.email == filed.data).first()
        if user:
            return jsonify(resFail("邮箱已经存在"))



class checkcode(Error):
    checkcode=StringField(validators=[Length(message="长度必须是6-60",min=6,max=60),InputRequired(message="验证码不能为空")])
    def valide_email(self,filed):
        checkcode1=getmem(filed.data)
        if not checkcode or checkcode != filed.data.upper():
            return jsonify(resFail("请输入正确的验证码"))
