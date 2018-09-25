from flask import Blueprint,render_template,request,jsonify,session
from apps.cms.checkForm import *
from apps.cms.model import *
from ext import db
from flask.views import MethodView
from apps.common.response import *
bp=Blueprint("bp",__name__,url_prefix="/cms")
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
def index():
    logindata=session.get("checklogin",None)#使用get+默认值的话并不会出现键值为空的情况
    if logindata:
        return render_template("cms/index.html")
    else:
        return render_template("cms/login.html")

@bp.route("/logout/")
def logout():
    session.clear()
    return render_template("cms/login.html")
@bp.route("/user_info/")
def user_info():
    return render_template("cms/personal.html")

class resetpwd(MethodView):
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
    def get(self):
        pass
    def post(self):
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
