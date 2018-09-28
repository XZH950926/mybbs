"""第三方软件的初始化"""
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
mail=Mail()