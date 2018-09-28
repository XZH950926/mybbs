from flask import Blueprint,render_template,request,jsonify,session,redirect
from apps.cms.checkForm import *
from apps.cms.model import *
from ext import db,mail
from flask_mail import Message
from flask.views import MethodView
from apps.common.response import *
from apps.common.memcached import *
import string,random
from functools import wraps
bp=Blueprint("bp",__name__,url_prefix="/cms")

def permisionresist(permis):
    def outer(func):
        @wraps(func)
        def inner(*args,**kwargs):
            user_id=session["user_id"]
            user = User.query.get(user_id)
            r = user.checkpermission(permis)
            func(*args,**kwargs)
        return inner
    return outer


def resistLogin(func):
    @wraps(func) #白函数直接可以当做属性来调用
    def inner(*args,**kwargs):
        logindata = session.get("checklogin", None)  # 使用get+默认值的话并不会出现键值为空的情况
        if logindata:
            return func(*args,**kwargs)
        else:
            return redirect("/cms/")
    return inner

@bp.route("/")
def cms_dp():
    return render_template("/cms/login.html")

@bp.route("/login/",methods=["post"])
def login():
    fm=checkForm(formdata=request.form)
    if fm.validate():
        password=fm.password.data
        email=fm.email.data
        user=db.session.query(User).filter(User.email==email).first()
        if not user:
            return jsonify(resFail("用户不存在"))
        if not user.checkPwd(password):
            return jsonify(resFail("密码错误"))
        else:
            session["checklogin"] = "login"
            session["user_id"]=user.id
            ischecked=request.values.get("ischeck")
            if ischecked=="1":
                session.permanent = True
            return jsonify(resSuccess())
    else:
        return jsonify(resFail(fm.err))

@bp.route("/index/")
@resistLogin
def index():
    # logindata=session.get("checklogin",None)#使用get+默认值的话并不会出现键值为空的情况
    # if logindata:
    return render_template("cms/index.html")
    # else:
    #     return render_template("cms/login.html")

@bp.route("/logout/")
@resistLogin
def logout():
    session.clear()
    return render_template("cms/login.html")


@bp.route("/user_info/")
@resistLogin
@permisionresist(1)
def user_info():
    return render_template("cms/personal.html")

class resetpwd(MethodView):
    decorators = [resistLogin,permisionresist(1)]
    def get(self):
        return render_template("cms/resetpassword.html")
    def post(self):
        fm=resetpwdForm(formdata=request.form)
        if fm.validate():
            password1=fm.password1.data
            password2=fm.password2.data
            user = db.session.query(User).filter(User.id == session["user_id"]).first()
            if user.checkPwd(password1):
                user.password=password2
                db.session.commit()
                return jsonify(resSuccess("修改成功"))
            else:
                return jsonify(resFail("旧密码不对"))
        else:
            return jsonify(resFail(fm.err))

class resetemail(MethodView):
    decorators = [resistLogin,permisionresist(1)]
    def get(self):
       return render_template("cms/resetemail.html")
    def post(self):
        fm = checkcode(formdata=request.form)
        if fm.validate():
            # email = fm.email.data
            # user = User.query.filter(User.email == email).first()
            # if not user:
            #     mememailcode = getmem(fm.email.data)
            #     checkcode=request.values.get("checkcode")
            #     if not mememailcode or mememailcode != checkcode.upper():
            #         return jsonify(resFail("请输入正确的验证码"))
            #     else:
                    user=User.query.filter(User.id==session.get("user_id")).first()
                    email=request.values.get("email")
                    user.email=email
                    db.session.commit()
                    return jsonify(resSuccess("邮箱修改成功"))
        else:
            return jsonify(resFail(data=fm.err))


@bp.route("/send_checkcode/",methods=["post"])
@resistLogin
@permisionresist(1)
def send_checkcode():
    fm = resetEmail(formdata=request.form)
    if fm.validate():
        # 查询邮箱有没有
            r = string.ascii_letters + string.digits
            r = ''.join(random.sample(r, 6))
            setmem(fm.email.data, r.upper(), 30 * 60)
            msg = Message("更新邮箱验证码", recipients=[fm.email.data], body="验证码为" + r)
            mail.send(msg)
            return jsonify(resSuccess(data='发送成功，请查看邮箱'))
    else:
        return jsonify(resFail(data=fm.err))

class banner(MethodView):#轮播图管理
    pass


bp.add_url_rule("/resetemail/",endpoint="resetemail",view_func=resetemail.as_view("resetemail"))
bp.add_url_rule("/resetpwd/",endpoint="resetpwd",view_func=resetpwd.as_view("resetpwd"))

@bp.context_processor
def getUser():
    login=session.get("checklogin")
    if login:
        user_id = session["user_id"]
        user = User.query.filter(User.id==user_id).first()
        return {"user":user}#会产生序列化问题
    else:
        return {}
