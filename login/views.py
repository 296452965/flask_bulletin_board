from flask import Blueprint, session, redirect, url_for, request, flash, render_template
from DBFunc import query_sql
bp = Blueprint('login', __name__, url_prefix='/')


# 登录页面，用户成功登录后进入展示页面
@bp.route('login/', methods=['GET', 'POST'])
def login():
    if session.get('role', None) == 'user':
        return redirect(url_for('user.index'))
    elif session.get('role', None) == 'admin':
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('password')
        role = request.form.get('role')
        if role == '1':  # 1代表管理员
            sql = 'SELECT count(*) AS Count FROM AdminInfo WHERE UserName=? and PassWord=?'
            result = query_sql(sql, (username, pwd), one=True)

            if int(result.get('Count')) > 0:
                session['username'] = username
                session['role'] = 'admin'
                return redirect(url_for('admin.index'))
            flash('用户名或密码错误！')
        if role == '0':  # 2代表用户
            sql = 'SELECT count(*) AS Count FROM UserInfo WHERE UserName=? and PassWord=?'
            result = query_sql(sql, (username, pwd), one=True)
            if int(result.get('Count')) > 0:
                session['username'] = username
                session['role'] = 'user'
                return redirect(url_for('user.index'))
            flash('用户名或密码错误！')
    return render_template('login.html')


# 退出，结束session，返回至登录页面
@bp.route('logout/')
def logout():
    session.clear()
    return redirect(url_for('login.login'))
