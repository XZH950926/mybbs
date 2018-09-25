from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length
#？
class Error(FlaskForm):
    @property
    def err(self):
        return self.errors.popitem()[1][0]

class checkForm(Error):
    password=StringField(validators=[Length(min=6,max=60,message="密码必须是6-60位"),InputRequired(message="密码不能为空")])
    email=StringField(validators=[Email(message="输入的必须是邮箱"),InputRequired(message="输入的不能为空")])