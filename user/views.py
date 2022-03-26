from flask import Blueprint, session, redirect, render_template, url_for
user = Blueprint('user', __name__, url_prefix='/user/')


# 管理员页面主页
@user.route('index/')
def index():
    return render_template('user/index.html')


# 个人信息编辑页面
@user.route('profile/')
def profile():
    return render_template('user/profile.html')