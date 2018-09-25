from flask import Blueprint,render_template,request,jsonify
from apps.cms.checkForm import *
from apps.cms.model import *
from ext import db
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
        per=db.session.query(User).filter(User.email==email).first()
        if not per:
            return jsonify(resFail("用户不存在"))
        if not per.checkPwd(password):
            return jsonify(resFail("密码错误"))
        else:
            return jsonify(resSuccess())
    else:
        return jsonify(resFail(fm.err))
@bp.route("/index/")
def index():
    return render_template("cms/index.html")


