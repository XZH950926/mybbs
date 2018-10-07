from flask import Blueprint,request,session,redirect
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
from apps.common.model import Banner,Border,Post,Common,Tag
#
from flask_paginate import Pagination,get_page_parameter
from functools import wraps
from ext import db
bp = Blueprint('front',__name__)


#装饰器用来限制登录
def outer(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if session.get("user_id",None):
            return func(*args,**kwargs)
        else:
            return render_template("front/login.html")
    return inner

@bp.route("/")
def loginView():
    banners = Banner.query.order_by(Banner.priority.desc()).limit(4)
    borders=Border.query.all()

    page1=request.args.get(get_page_parameter(),type=int,default=1)
    start=(page1-1)*3
    end=start+3
    border_id= request.values.get("border_id")
    new=request.args.get("new")
    views=request.args.get("views")
    good=request.args.get("good")
    jinhua=request.args.get("jinhua")
    if not border_id:
        if views:
            count = Post.query.count()
            posts = Post.query.order_by(Post.views.desc(),Post.create_time.desc()).slice(start, end)
            pagination = Pagination(bs_version=3, page=page1, total=count, per_page=3)
        if jinhua:
            count = Post.query.count()
            posts = Post.query.outerjoin(Tag, Post.id == Tag.post_id).order_by(Tag.create_time.desc()).all()
            pagination = Pagination(bs_version=3, page=page1, total=count, per_page=3)
        else:
            count = Post.query.count()
            posts = Post.query.order_by( Post.create_time.desc()).slice(start, end)
            pagination = Pagination(bs_version=3, page=page1, total=count, per_page=3)
    else:
        if views:
            posts = Post.query.filter(Post.border_id == border_id).order_by(Post.views.desc(),Post.create_time.desc()).slice(start,end)
            count = Post.query.filter(Post.border_id == border_id).count()
            pagination = Pagination(bs_version=3, page=page1, total=count, per_page=3)
        else:
            posts = Post.query.filter(Post.border_id == border_id).order_by(Post.create_time.desc()).slice(start, end)
            count = Post.query.filter(Post.border_id == border_id).count()
            pagination = Pagination(bs_version=3, page=page1, total=count, per_page=3)

    context={
        "banners":banners,
        "borders":borders,
        "posts":posts,
        "pagination":pagination
    }
    return render_template("front/index.html",**context)

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
                session["user_id"]=user.id
                session.permanent = True
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



class addpost(MethodView):
    decorators = [outer]
    def get(self):
        borders=Border.query.all()
        context={
           "borders":borders
        }
        return render_template("front/addpost.html",**context)
    def post(self):
        fm=postForm(formdata=request.form)
        if fm.validate():
            user_id=session.get("user_id")
            if user_id:
                post=Post(title=fm.title.data,user_id=user_id,content=fm.content.data,border_id=fm.border_id.data)
                db.session.add(post)
                db.session.commit()
                return jsonify(resSuccess(data="创建帖子成功"))
            else:
                return jsonify(resFail(data="请先登录"))
        else:
            return jsonify(resFail(fm.err))

@bp.route("/logout/")
def logout():
    session.clear()
    return render_template("front/login.html")


@bp.context_processor
def getUser():
    user_id=session.get("user_id",None)
    if user_id:
        user=Front_USER.query.filter(Front_USER.id==user_id).first()
        return {"user":user}
    else:
        return {"user":None}


@bp.route("/showpostcontent/")
def showpostcontent():
    post_id=request.values.get("post_id")
    post=Post.query.filter(Post.id==post_id).first()
    commons=Common.query.filter(Common.post_id==post_id)
    if not post.views:
        post.views=0
        post.views+=1
        db.session.commit()
    else:
        post.views+=1
        db.session.commit()
    context={
        "post":post,
        "commons":commons
    }
    return render_template("front/showpost.html",**context)


@outer
@bp.route("/addcommon/",methods=["post"])
def addcommon():
    # 判断用户有没有登录
    # 获取当前用户的id
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify(resFail(data="请先登录"))
    # 获取帖子的id
    post_id = request.values.get("post_id")
    # 获取评论的内容
    content = request.values.get("content")
    if not content:
        return jsonify(resFail(data="评论不能为空"))
    # 在数据库中插入
    commom = Common(content=content, post_id=post_id, user_id=user_id)
    db.session.add(commom)
    db.session.commit()
    return jsonify(resSuccess(data="评论成功"))


bp.add_url_rule("/addpost/",endpoint="addpost",view_func=addpost.as_view("addpost"))
bp.add_url_rule("/findpwd/",endpoint="findpwd",view_func=findpwd.as_view("findpwd"))
bp.add_url_rule("/signup/",endpoint='signup',view_func=Signup.as_view('signup'))
bp.add_url_rule("/signin/",endpoint="signin",view_func=signin.as_view("signin"))

