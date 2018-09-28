from flask import Blueprint,request,session
from flask import render_template
from flask.views import MethodView
from apps.front.forms import *
import string
import random
from io import BytesIO
from dysms_python.demo_sms_send import send_sms
from flask import jsonify
from apps.common.response import *
import json
from flask import make_response
from apps.common.captcha.xtcaptcha import Captcha
from apps.common.memcached import getmem,setmem,delete
#
from ext import db
bp = Blueprint('front',__name__)

@bp.route("/")
def loginView():
    return render_template("front/index.html")

class Signup(MethodView):
    def get(self):
        loc=request.headers.get("Referer")
        if loc:
            location=loc
        else:
            location="/"
        context={
            "location":location
        }
        return render_template("front/signup.html",**context)
    def post(self):
        fm=SignupFrom(formdata=request.form)
        if fm.validate():
            print("aa")
            u=Front_USER(username=fm.username.data,password=fm.password.data,
                         telephone=fm.telephone.data)
            db.session.add(u)
            db.session.commit()
            delete(fm.telephone.data)  # 注册成功，删除手机验证码
            return jsonify(resSuccess("注册成功"))
        else:
            return jsonify(resFail(fm.err))

@bp.route("/send_sms_code/",methods=['post'])
def sendSMSCode():
    fm = checktelphone(formdata=request.form)
    if fm.validate():
        #生成验证码
        r = string.digits
        r = ''.join(random.sample(r, 4))
        #发送验证码
        r1 = send_sms(phone_numbers=fm.telephone.data,smscode=r) #b'{"Message":"OK","RequestId":"26F47853-F6CD-486A-B3F7-7DFDCE119713","BizId":"102523637951132428^0","Code":"OK"}'
        if  json.loads(r1.decode("utf-8"))['Code'] == 'OK':
            setmem(fm.telephone.data,r, 30 * 60)
            print(r)
            return jsonify(resSuccess(data="短信验证码发送成功，请查收"))
        else:  # 发送失败
            return jsonify(resFail(data="请检查网络"))
    else:
        return jsonify(resFail(data=fm.err))

#通过前端src访问的地址的不断变化进行不断访问
@bp.route("/captcha/")
def ImgCode():
    #生成6位的字符串
    #把这个字符添加到图片上
    #用特殊字符
    #添加横线
    #添加噪点
    text, img = Captcha.gene_code()  # 通过工具类生成验证码
    print(text)
    out = BytesIO()  # 初始化流对象
    img.save(out, 'png')  # 保存成png格式
    out.seek(0)  # 从文本的开头开始读
    setmem(text, text.upper(), 60)
    resp = make_response(out.read())  # 根据流对象生成一个响应
    resp.content_type = "image/png"  # 设置响应头中content-type
    return resp

class signin(MethodView):
    def get(self):
        return render_template("front/login.html")
    def post(self):
        fm=checkLogin(formdata=request.form)
        if fm.validate():
            user=Front_USER.query.filter(Front_USER.telephone==fm.telephone.data).first()
            if user.checkPwd(fm.password.data):
                return jsonify(resSuccess(data="登陆成功"))
            else:
                return jsonify(resFail(data="密码出错了"))
        else:
            return jsonify(resFail(fm.err))


class findpwd(MethodView):
    def get(self):
        return render_template("front/findpwd.html")
    def post(self):
        fm = change_pwd(formdata=request.form)
        if fm.validate():
            u=Front_USER.query.filter(Front_USER.telephone==fm.telephone.data).first()
            u.password=fm.password.data
            db.session.commit()
            delete(fm.telephone.data)  # 注册成功，删除手机验证码
            return jsonify(resSuccess("注册成功"))
        else:
            return jsonify(resFail(fm.err))


@bp.route("/change_pwd_sms/",methods=["post"])
def change_pwd_sms():
    fm = pwd_telephone(formdata=request.form)
    if fm.validate():
        # 生成验证码
        r = string.digits
        r = ''.join(random.sample(r, 4))
        # 发送验证码
        r1 = send_sms(phone_numbers=fm.telephone.data,
                      smscode=r)  # b'{"Message":"OK","RequestId":"26F47853-F6CD-486A-B3F7-7DFDCE119713","BizId":"102523637951132428^0","Code":"OK"}'
        if json.loads(r1.decode("utf-8"))['Code'] == 'OK':
            setmem(fm.telephone.data, r.upper(), 30 * 60)
            print(r)
            return jsonify(resSuccess(data="短信验证码发送成功，请查收"))
        else:  # 发送失败
            return jsonify(resFail(data="请检查网络"))
    else:
        return jsonify(resFail(data=fm.err))




bp.add_url_rule("/findpwd/",endpoint="findpwd",view_func=findpwd.as_view("findpwd"))
bp.add_url_rule("/signup/",endpoint='signup',view_func=Signup.as_view('signup'))
bp.add_url_rule("/signin/",endpoint="signin",view_func=signin.as_view("signin"))

