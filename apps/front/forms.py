from flask_wtf import FlaskForm
from apps.common.memcached import setmem,getmem
from wtforms import StringField,IntegerField
from wtforms.validators import Regexp,ValidationError,InputRequired,Length,EqualTo
from apps.front.model import Front_USER
from flask import jsonify
from apps.common.response import *
class BaseForm(FlaskForm):
    @property    # 把函数变成了属性来调用
    def err(self):
        return self.errors.popitem()[1][0]
class checktelphone(BaseForm):
    telephone=StringField(validators=[Regexp("^1[35768]\d{9}$",message="必须输入正确的电话号码"),])
    def validate_telephone(self,filed):
        user=Front_USER.query.filter(Front_USER.telephone==filed.data).first()
        if user:
            raise ValidationError("该电话号码已经被注册")

class SignupFrom(checktelphone):
    username = StringField(validators=[InputRequired(message="必须输入用户名"),Length(min=6,max=20,message="用户名必须是6-20位")])
    password = StringField(validators=[InputRequired(message="必须输入密码"),Length(min=6,max=20,message="密码必须是6-20位")])
    password1 = StringField(validators=[EqualTo('password',message="两次密码必须一致")])
    smscode = StringField(validators=[InputRequired(message="必须输入手机验证码")])
    captchacode = StringField(validators=[InputRequired(message="必须输入图片验证码")])

    def validate_username(self,filed):
        user=Front_USER.query.filter(Front_USER.username==filed.data).first()
        if user:
            raise ValidationError("用户已经存在")

    def validate_smscode(self,filed):
        code=getmem(self.telephone.data)
        if not code:
            raise ValidationError("请输入正确的短信验证码")
        if code!=filed.data.upper():
            raise ValidationError("请输入正确的短信验证码")

    def validate_captchacode(self,filed):
        code2=getmem(filed.data.upper())
        if not code2:
            raise ValidationError("请输入正确的图片验证码")

class pwd_telephone(BaseForm):
    telephone=StringField(validators=[Length(min=11,message="电话号码必须是11位"),InputRequired(message="号码输入不能为空"),Regexp("^1[35789]\d{9}$",message="必须输入正确的号码")])
    def validate_telephone(self, filed):
        user = Front_USER.query.filter(Front_USER.telephone == filed.data).first()
        if not user:
            raise ValidationError("该电话号码没有被注册,请先注册")


class checkLogin(BaseForm):
    telephone=StringField(validators=[Length(min=11,message="电话号码必须是11位"),InputRequired(message="号码输入不能为空"),Regexp("^1[35789]\d{9}$",message="必须输入正确的号码")])
    password=StringField(validators=[Length(min=6,max=20,message="密码必须是6-20位"),InputRequired(message="密码不能为空")])
    def validate_telephone(self,filed):
        user=Front_USER.query.filter(Front_USER.telephone==filed.data)
        if not user:
            return jsonify(resFail(data="对不起,该号码未被注册"))

class change_pwd(BaseForm):
    password = StringField(validators=[InputRequired(message="必须输入密码"), Length(min=6, max=20, message="密码必须是6-20位")])
    password1 = StringField(validators=[EqualTo('password', message="两次密码必须一致")])
    smscode = StringField(validators=[InputRequired(message="必须输入手机验证码")])
    telephone=StringField(validators=[Length(min=11,message="电话号码必须是11位"),InputRequired(message="号码输入不能为空"),Regexp("^1[35789]\d{9}$",message="必须输入正确的号码")])
    def validate_smscode(self, filed):
        code = getmem(self.telephone.data)
        if not code:
            return jsonify(resFail(data="请输入正确的短信验证码"))
        if code != filed.data.upper():
            return jsonify(resFail(data="请输入正确的短信验证码"))

class postForm(BaseForm):
    title = StringField(InputRequired(message="帖子标题不能为空"))
    border_id = IntegerField(InputRequired(message="板块不能为空"))
    content = StringField(InputRequired(message="帖子内容不能为空"))




