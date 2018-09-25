from flask import Blueprint
bp=Blueprint("bp",__name__)
@bp.route("/login/")
def login():
    pass