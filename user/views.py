from flask import Blueprint, session, redirect, render_template, url_for, flash, request
from flask_login import login_required, current_user
from admin.models import Content

user = Blueprint('user', __name__, url_prefix='/user/')


# 用户页面主页
@user.route('index/')
@login_required
def index():
    uid = current_user.uid
    per_page = 10
    page = int(request.args.get('page', 1))
    contents = Content.query.filter_by(uid=uid).paginate(page, per_page)
    return render_template('user/index.html', contents=contents)


# 个人信息编辑页面
@user.route('profile/')
@login_required
def profile():
    return render_template('user/profile.html')
