
class respon():
    def __init__(self,code,message,data=None):
        self.code=code
        self.message=message
        self.data=data
class showResponseInfo():
    success=200
    fail=400
    argumentErr=401

def resSuccess(data=None):
    return respon(200,"登陆成功",data).__dict__
def resFail(data):
    return respon(400,"登录失败",data=data).__dict__
def argumentErr(data):
    return respon(401,"参数错误",data=data).__dict__

