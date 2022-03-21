from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from flask.views import MethodView
from exts import db
from models import DataBar, DataLine, Content, Category1, Category2, Unit

bp = Blueprint('user', __name__, url_prefix='/user/')


# 函数视图
# Ajax响应二级列表
@bp.route('changeselectfield', methods=['GET', 'POST'])
def changeselectfield():
    if request.method == "POST":
        data = request.get_json()
        c1id = data['c1id']
        li = []
        for c in Category2.query.filter_by(c1id=c1id).all():
            dic = {}
            dic['id'] = c.id
            dic['category'] = c.category
            li.append(dic.copy())
        print("!!!!!!!!!!!")
        return jsonify(li)
    else:
        return {}


# 用户首页
@bp.route('index/')
def index():
    if session.get('role', None) == 'user':
        return render_template('index.html')
    else:
        return redirect(url_for('login.login'))


# 获取首页柱形图数据
@bp.route('index/bar', methods=["get"])
def index_bar():
    li = []
    for c in DataBar.query.all():
        dic = {}
        dic['data'] = c.data
        dic['label'] = c.label
        li.append(dic.copy())
    print(li)
    return jsonify(li)


# 获取首页线形图数据
@bp.route('index/line', methods=["get"])
def index_line():
    li = []
    for c in DataLine.query.all():
        dic = {}
        dic['data'] = c.data
        dic['label'] = c.label
        li.append(dic.copy())
    print(li)
    return jsonify(li)


# 页面二
@bp.route('analysis/')
def analysis():
    return render_template('analysis.html')


# 个人信息编辑页面
@bp.route('profile/')
def profile():
    return render_template('profile.html')


# 类视图
# 页面一
class DetailView(MethodView):
    @staticmethod
    def get():
        # 前端传参unit,category1,category2,page,datefilter
        uid = int(request.args.get('unit')) if request.args.get('unit') else None
        c1id = int(request.args.get('category1')) if request.args.get('category1') else None
        c2id = int(request.args.get('category2')) if request.args.get('category2') else None
        page = int(request.args.get('page', 1))  # 获取第‘page’页数据
        # 分割日期范围,datefilter[0]：开始时间；datefilter[1]：结束时间
        datefilter = request.args.get('datefilter').split(' - ') if  request.args.get('datefilter') else None
        per_page = 10  # 数据分页，每页显示2条数据
        # 根据参数选择查询过滤方式
        if c2id:
            if uid:
                paginate = Content.query.filter_by(uid=uid, c1id=c1id, c2id=c2id)
            else:
                paginate = Content.query.filter_by(c1id=c1id, c2id=c2id)
        else:
            if c1id:
                if uid:
                    paginate = Content.query.filter_by(uid=uid, c1id=c1id)
                else:
                    paginate = Content.query.filter_by(c1id=c1id)
            else:
                if uid:
                    paginate = Content.query.filter_by(uid=uid)
                else:
                    paginate = Content.query.filter_by()
        if datefilter:
            paginate = paginate.filter(Content.date.between(datefilter[0], datefilter[1])).paginate(page, per_page)
        else:
            paginate = paginate.paginate(page, per_page)
        contents = paginate.items
        print(contents)
        category1s = db.session.query(Category1)
        units = Unit.query.all()
        return render_template('detail.html', contents=contents, paginate=paginate, category1s=category1s, units=units,
                               uid=uid, c1id=c1id, c2id=c2id)


# 测试页，使用类视图方法写
class TestView(MethodView):
    @staticmethod
    def get():
        # 前端传参unit=1&category1=1&category2=1
        uid = int(request.args.get('unit')) if request.args.get('unit') else None
        c1id = int(request.args.get('category1')) if request.args.get('category1') else None
        c2id = int(request.args.get('category2')) if request.args.get('category2') else None
        page = int(request.args.get('page', 1))  # 获取第‘page’页数据
        per_page = 2  # 数据分页，每页显示2条数据
        if c2id:
            if uid:
                paginate = Content.query.filter_by(uid=uid, c1id=c1id, c2id=c2id).paginate(page, per_page)
            else:
                paginate = Content.query.filter_by(c1id=c1id, c2id=c2id).paginate(page, per_page)
        else:
            if c1id:
                if uid:
                    paginate = Content.query.filter_by(uid=uid, c1id=c1id).paginate(page, per_page)
                else:
                    paginate = Content.query.filter_by(c1id=c1id).paginate(page, per_page)
            else:
                if uid:
                    paginate = Content.query.filter_by(uid=uid).paginate(page, per_page)
                else:
                    paginate = Content.query.paginate(page, per_page)
        contents = paginate.items
        category1s = db.session.query(Category1)
        units = Unit.query.all()
        return render_template('test.html', contents=contents, paginate=paginate, category1s=category1s, units=units,
                               uid=uid, c1id=c1id, c2id=c2id)


# 信息填报页面
class AddView(MethodView):
    @staticmethod
    def get():
        category1s = db.session.query(Category1)
        units = Unit.query.all()
        return render_template('add.html', category1s=category1s, units=units)

    @staticmethod
    def post():
        uid = request.form['unit']
        c1id = request.form['category1']
        c2id = request.form['category2']


bp.add_url_rule('add/', view_func=AddView.as_view('add'))
bp.add_url_rule('test/', view_func=TestView.as_view('test'))
bp.add_url_rule('detail/', view_func=DetailView.as_view('detail'))