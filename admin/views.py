from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for, flash, send_file
from flask.views import MethodView
from flask_login import login_required, current_user
from io import BytesIO
from functools import wraps
import time
import xlsxwriter

from exts import db
from admin.models import DataBar, DataLine, Content, Category1, Category2, Unit

admin = Blueprint('admin', __name__, url_prefix='/admin/')


def is_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.is_authentic:
            if current_user.role != 1:
                flash('非管理员无法访问该页面')
                return redirect(url_for('login.login'))
        return f(*args, **kwargs)

    return wrapper()


# 函数视图(FBV)
# Ajax响应二级列表
@admin.route('change_select_field', methods=['GET', 'POST'])
def change_select_field():
    if request.method == "POST":
        data = request.get_json()
        c1id = data['c1id']
        li = []
        for c in Category2.query.filter_by(c1id=c1id).all():
            dic = {}
            dic['id'] = c.id
            dic['category'] = c.category
            li.append(dic.copy())
        return jsonify(li)
    else:
        return {}


# Ajax获取首页柱形图数据
@admin.route('index/bar', methods=["get"])
def index_bar():
    li = []
    for c in DataBar.query.all():
        dic = {}
        dic['data'] = c.data
        dic['label'] = c.label
        li.append(dic.copy())
    # print(li)
    return jsonify(li)


# Ajax获取首页线形图数据
@admin.route('index/line', methods=["get"])
def index_line():
    li = []
    for c in DataLine.query.all():
        dic = {}
        dic['data'] = c.data
        dic['label'] = c.label
        li.append(dic.copy())
    # print(li)
    return jsonify(li)


# 个人信息编辑页面
@admin.route('profile/')
@login_required
def profile():
    return render_template('admin/profile_admin.html')


# 图表分析页面
@admin.route('analysis/')
@login_required
def analysis():
    return render_template('admin/content_analysis.html')


# 管理员首页
@admin.route('index/')
@login_required
# @is_admin
def index():
    return render_template('admin/index_admin.html')


# 类视图(CBV)
# 信息查询页面
class DetailView(MethodView):
    @staticmethod
    @login_required
    def get():
        # 前端传参unit,category1,category2,page,datefilter
        # flash(current_user.role)
        # flash(current_user.username)
        uid = int(request.args.get('unit')) if request.args.get('unit') else None
        c1id = int(request.args.get('category1')) if request.args.get('category1') else None
        c2id = int(request.args.get('category2')) if request.args.get('category2') else None
        modificationstate = bool(int(request.args.get('modificationstate'))) if request.args.get(
            'modificationstate') else None
        page = int(request.args.get('page', 1))  # 获取第‘page’页数据
        # 分割日期范围,datefilter[0]：开始时间；datefilter[1]：结束时间
        datefilter = request.args.get('datefilter').split(' - ') if request.args.get('datefilter') else None
        per_page = 10  # 数据分页，每页显示10条数据
        # 根据问题分类选择确定过滤方式
        if c2id:
            paginate = Content.query.filter_by(c1id=c1id, c2id=c2id)
        elif c1id:
            paginate = Content.query.filter_by(c1id=c1id)
        else:
            paginate = Content.query.filter_by()
        # 根据是否选择单位确定过滤方式
        if uid:
            paginate = paginate.filter_by(uid=uid)
        # 根据是否选择整改状态确定过滤方式
        if modificationstate:
            paginate = paginate.filter_by(modificationstate=modificationstate)
        # 根据是否选择日期范围确定过滤方式
        if datefilter:
            paginate = paginate.filter(Content.date.between(datefilter[0], datefilter[1]))
        paginate = paginate.paginate(page, per_page)
        category1s = db.session.query(Category1)
        units = Unit.query.all()
        return render_template('admin/content_detail.html', paginate=paginate, category1s=category1s,
                               units=units, uid=uid, c1id=c1id, c2id=c2id)


# 信息填报页面
class AddView(MethodView):
    @staticmethod
    @login_required
    def get():
        category1s = db.session.query(Category1)
        units = Unit.query.all()
        return render_template('admin/content_add.html', category1s=category1s, units=units)

    @staticmethod
    @login_required
    def post():
        uid = request.form['unit']
        c1id = request.form['category1']
        c2id = request.form['category2']
        date = request.form['date']
        problem = request.form['problem']
        content = Content(problem, c1id, c2id, uid, date, modificationstate=0, modificationdate=None)
        db.session.add(content)
        db.session.commit()
        if content.id is not None:
            flash(f'您已成功添加第{content.id}条数据')
        return redirect(url_for('admin.add'))


# 信息删除页面
class DelView(MethodView):
    @staticmethod
    @login_required
    def get(id=None):
        del_con = Content.query.filter_by(id=id).first()
        db.session.delete(del_con)
        db.session.commit()
        flash('信息删除成功')
        return redirect(url_for('admin.detail'))


# 信息修改页面
class UpdateView(MethodView):
    @staticmethod
    @login_required
    def post():
        content_id = request.form['id']
        date = request.form['modificationdate']
        state = 1 if request.form['modificationstate'] == 'on' else 0
        edit_con = Content.query.filter_by(id=content_id).first()
        edit_con.modificationstate = state
        edit_con.modificationdate = date
        db.session.commit()
        flash('信息修改成功')
        return redirect(url_for('admin.detail'))


# 列表导出
class ExportView(MethodView):
    @staticmethod
    @login_required
    def get():
        out = BytesIO()
        # !!!!!注释是将导出数据保存到本地磁盘，路径设置改到setting文件中
        # file_path = os.getcwd() + '\\static\\excel\\'  # 绝对路径
        # file_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "数据.xlsx"
        # workbook = xlsxwriter.Workbook(file_path + file_name)
        workbook = xlsxwriter.Workbook(out)
        worksheet = workbook.add_worksheet("数据")
        worksheet.set_column('A:H', 20)
        worksheet.write('A1', 'ID')
        worksheet.write('B1', '单位')
        worksheet.write('C1', '分类一')
        worksheet.write('D1', '分类二')
        worksheet.write('E1', '问题')
        worksheet.write('F1', '日期')
        worksheet.write('G1', '整改状态')
        worksheet.write('H1', '整改日期')
        contents = Content.query.order_by(Content.date.desc()).all()
        if contents is not None:
            for i in range(len(contents)):
                content = contents[i]
                lst_content = [content.id, content.unit.unitname, content.category1.category,
                               content.category2.category, content.problem, content.date, content.modificationstate,
                               content.modificationdate]
                worksheet.write_row(i + 1, 0, lst_content)
        workbook.close()
        out.seek(0)
        file_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "数据.xlsx"
        res = send_file(out, as_attachment=True, attachment_filename=file_name)
        return res


admin.add_url_rule('add/', view_func=AddView.as_view('add'))
admin.add_url_rule('del/<id>/', view_func=DelView.as_view('delete_content'))
admin.add_url_rule('detail/', view_func=DetailView.as_view('detail'))
admin.add_url_rule('edit/', view_func=UpdateView.as_view('edit_content'))
admin.add_url_rule('detail/export/', view_func=ExportView.as_view('export_data'))
