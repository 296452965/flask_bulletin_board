from flask import Blueprint, session, redirect, url_for, request, flash, render_template
from flask_login import login_user, logout_user, login_required
from app.department.models import Department
from . import bp


# 登录页面，使用flask-login
@bp.route('login/', methods=['GET', 'POST'])
def login():
    if session.get('role', None) == 'user':
        return redirect(url_for('user.index'))
    elif session.get('role', None) == 'admin':
        return redirect(url_for('admin.index'))
    elif request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('password')
        role = request.form.get('role')
        if role == '2':  # 2代表管理员
            result = Department.query.filter_by(username=username, rid=role).first()
            if result is not None and result.validate_password(pwd):
                login_user(result)
                session['username'] = username
                session['role'] = 'admin'
                next = request.args.get('next')
                return redirect(next or url_for('admin.index'))  # 必须验证next参数的值。如果不验证的话，应用将会受到重定向的攻击。
            flash('用户名或密码错误！')
        if role == '1':  # 1代表用户
            result = Department.query.filter_by(username=username, rid=role).first()
            if result is not None and result.validate_password(pwd):
                login_user(result)
                session['username'] = username
                session['role'] = 'user'
                next = request.args.get('next')
                return redirect(next or url_for('user.index'))
            flash('用户名或密码错误！')
    return render_template('login/login.html')


# 退出，结束session，返回至登录页面
@bp.route('logout/')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login.login'))
