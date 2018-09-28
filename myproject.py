from flask import Flask
from flask_mail import Message
from ext import mail
import config
from ext import db
from apps.cms.view import bp as cms_bp
from apps.front.view import bp as front_bp
from flask_wtf import CSRFProtect
app=Flask(__name__)
app.config.from_object(config)
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
db.init_app(app)
CSRFProtect(app=app)
mail.init_app(app)

if __name__ == '__main__':
    app.run()