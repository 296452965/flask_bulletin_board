from flask import Flask, redirect, url_for
from flask_migrate import Migrate  # ORM迁移，修改ORM对应的模型，然后再把模型映射到数据库中
from exts import db  # 避免循环引用
import login.views
import admin.views
import user.views
import settings
from wsgiref.simple_server import make_server

app = Flask(__name__, static_url_path='')
app.config.from_object(settings)  # 导入参数设置
app.register_blueprint(login.views.bp)  # 注册登录页面视图
app.register_blueprint(admin.views.admin)  # 注册管理员页面视图
app.register_blueprint(user.views.user)  # 注册用户页面视图
db.init_app(app)  # 初始化绑定app对象
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return redirect(url_for('login.login'))


if __name__ == '__main__':
    # server = make_server('0.0.0.0', 5000, app)
    # server.serve_forever()
    app.run()
