from flask import Blueprint, session, redirect, render_template, url_for
bp = Blueprint('admin', __name__, url_prefix='/admin/')


# 管理员页面主页
@bp.route('index/')
def index():
    return render_template('index_admin.html')