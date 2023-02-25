from flask import session, redirect, url_for, flash
from functools import wraps


def is_admin(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('role', None) != 'admin':
            flash('非法访问')
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)

    return wrapper

