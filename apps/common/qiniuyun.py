from flask import jsonify,Blueprint
bp=Blueprint("common_bp",__name__,url_prefix="/common")
from qiniu import Auth
# 应该写common中，因为这个视图函数，前后台都要使用
# 给客户端返回上传的令牌（token），因为
@bp.route("/qiniu_token/")
def qiniukey():
    # 通过secer-key id 生成一个令牌，返回给客户端
    ak = "gixRZTC9nnM_ODSEyAmDtFPVBD5sBWJo1dsfszvB"
    sk = "X8TYRWzELi-hfyzl1MeAkEbS9i5DKL_8qI4m_o3l"
    q = Auth(ak, sk)
    bucket_name = 'pjssb' # 仓库的名字
    token = q.upload_token(bucket_name)
    return jsonify({'uptoken': token})
