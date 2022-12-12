import os
from flask import Flask, url_for, redirect
from flask_login import LoginManager
from flask_migrate import Migrate

from config import config
from app.department.models import db


def create_app(config_name=None):
    app = Flask(__name__, static_url_path='')
    configure_app(app, config_name)  # 导入参数设置
    db.init_app(app)  # 初始化绑定app对象
    migrate = Migrate(app, db)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login.login'
    login_manager.login_message = '访问页面需要登录'

    @login_manager.user_loader
    def load_user(user_id):
        # from .department.models import Department
        from app.department.models import Department
        dep = Department.query.get(int(user_id))
        return dep

    # 引入蓝图并注册
    from app import login, admin, user, department, commands
    app.register_blueprint(login.bp)  # 注册登录页面视图
    app.register_blueprint(admin.admin)  # 注册管理员页面视图
    app.register_blueprint(user.user)  # 注册用户页面视图
    app.register_blueprint(department.department)  # 注册部门管理页面视图
    app.register_blueprint(commands.bp)  # 注册部门管理页面视图

    # 注册首页路由
    @app.route('/')
    def hello_world():
        return redirect(url_for('login.login'))

    return app


def configure_app(app, config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    if config_name in config:
        app.config.from_object(config[config_name])

