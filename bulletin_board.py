from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_migrate import Migrate  # ORM迁移，修改ORM对应的模型，然后再把模型映射到数据库中
from department.models import db
import login.views
import admin.views
import user.views
import department.views
import settings

app = Flask(__name__, static_url_path='')
app.config.from_object(settings)  # 导入参数设置
app.register_blueprint(login.views.bp)  # 注册登录页面视图
app.register_blueprint(admin.views.admin)  # 注册管理员页面视图
app.register_blueprint(user.views.user)  # 注册用户页面视图
app.register_blueprint(department.views.department)
db.init_app(app)  # 初始化绑定app对象
login_manager = LoginManager(app)
login_manager.login_view = 'login.login'
login_manager.login_message = '访问页面需要登录'
migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    from department.models import Department
    dep = Department.query.get(int(user_id))
    return dep


@app.route('/')
def hello_world():
    return redirect(url_for('login.login'))


if __name__ == '__main__':
    app.run()
