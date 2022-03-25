from flask import Flask, redirect, url_for, render_template
from flask_migrate import Migrate  # ORM迁移，修改ORM对应的模型，然后再把模型映射到数据库中
from exts import db  # 避免循环引用
import login.views
import user.views
import admin.views
import settings
from wsgiref.simple_server import make_server

app = Flask(__name__, static_url_path='')
app.config.from_object(settings)
app.register_blueprint(login.views.bp)
app.register_blueprint(user.views.bp)
app.register_blueprint(admin.views.bp)
db.init_app(app)  # 初始化绑定app对象
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return render_template('hello_world.html')


if __name__ == '__main__':
    # server = make_server('0.0.0.0', 5000, app)
    # server.serve_forever()
    app.run()
