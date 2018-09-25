from flask import Flask
import config
from ext import db
from apps.cms.view import bp as cms_bp
from flask_wtf import CSRFProtect
app=Flask(__name__)
app.config.from_object(config)
app.register_blueprint(cms_bp)
db.init_app(app)
CSRFProtect(app=app)

if __name__ == '__main__':
    app.run()