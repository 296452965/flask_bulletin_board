from flask import render_template, jsonify, request, session, redirect, url_for, flash, send_file, send_from_directory
from flask.views import MethodView
from flask_login import login_required, current_user
from io import BytesIO
import time
import xlsxwriter
import os
from app.decorators import is_admin
from . import admin
from .models import *
from .forms import DocumentForm
from config import UPLOAD_FOLDER


# 函数视图(FBV)
# 呈现特定目录下的资源
@admin.route('/document/<filename>')
@login_required
def render_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return '该文件不存在'


# Ajax响应二级列表
@admin.route('c2data', methods=['POST'])
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


# Ajax响应二级列表
@admin.route('case/pic', methods=['POST'])
def case_pic():
    if request.method == "POST":
        data = request.get_json()
        case_id = data['case_id']
        if 'praise_detail' in request.referrer:
            case = Praise.query.filter_by(id=case_id).first()
        else:
            case = Content.query.filter_by(id=case_id).first()
        if case.filepath:
            li = [i for i in (case.filepath.split(','))]
        else:
            li = []
        return jsonify(li)


# Ajax获取首页柱形图数据
@admin.route('index/bar', methods=["GET"])
def index_bar():
    li = []
    for c in DataBar.query.all():
        dic = {'data': c.data, 'label': c.label}
        li.append(dic.copy())
    return jsonify(li)


# Ajax获取首页线形图数据
@admin.route('index/line', methods=["GET"])
def index_line():
    li = []
    for c in DataLine.query.all():
        dic = {'data': c.data, 'label': c.label}
        li.append(dic.copy())
    return jsonify(li)


# 个人信息编辑页面
@admin.route('profile/')
@login_required
@is_admin
def profile():
    return render_template('admin/profile_admin.html')


# 图表分析页面
@admin.route('analysis/')
@login_required
@is_admin
def analysis():
    return render_template('admin/content_analysis.html')


# 管理员首页
@admin.route('index/')
@login_required
@is_admin
def index():
    print('role:', session.get('role'))
    return render_template('admin/index_admin.html')


# WebUploader上传页面
@admin.route('upload/', methods=['POST'])
@login_required
@is_admin
def upload():
    print(request.files)
    file_name_list = []
    for file in request.files.getlist('file'):
        file_name = file.filename
        file_name_list.append(file_name)
        filepath = os.path.join(UPLOAD_FOLDER, file_name)
        file.save(filepath)
    file_name_str = ','.join([x for x in file_name_list])
    ret = {
        'class': 'success',
        'status': 200,
        'info': '上传成功',
        'id': file_name_str,
    }
    return jsonify(ret)


# 类视图(CBV)
# 问题信息查询页面
class DetailView(MethodView):
    @staticmethod
    @login_required
    @is_admin
    def get():
        # 前端传参unit,category1,category2,page,datefilter
        # flash(current_user.role)
        # flash(current_user.username)
        clid = int(request.args.get('content_level')) if request.args.get('content_level') else None
        uid = int(request.args.get('unit')) if request.args.get('unit') else None
        c1id = int(request.args.get('category1')) if request.args.get('category1') else None
        c2id = int(request.args.get('category2')) if request.args.get('category2') else None
        modificationstate = int(request.args.get('modificationstate')) if request.args.get(
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
        # 根据是否选择分级确定过滤方式
        if clid:
            paginate = paginate.filter_by(clid=clid)
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
        content_levels = ContentLevel.query.all()
        return render_template('admin/content_detail.html', paginate=paginate, category1s=category1s,
                               units=units, content_levels=content_levels, uid=uid, c1id=c1id, c2id=c2id, clid=clid)


# 问题信息填报页面
class AddView(MethodView):
    @staticmethod
    @login_required
    @is_admin
    def get():
        category1s = db.session.query(Category1)
        units = Unit.query.all()
        content_levels = ContentLevel.query.all()
        return render_template('admin/content_add.html', category1s=category1s, units=units,
                               content_levels=content_levels)

    @staticmethod
    @login_required
    @is_admin
    def post():
        uid = request.form['unit']
        c1id = request.form['category1']
        c2id = request.form['category2']
        clid = request.form['content_level']
        date = request.form['date']
        case = request.form['case']
        filepath = request.form['pics']
        content = Content(case, c1id, c2id, uid, clid, date, modificationstate=0, modificationdate=None,
                          filepath=filepath)
        unit = Unit.query.filter_by(id=uid).first()
        content_level = ContentLevel.query.filter_by(id=clid).first()

        # 分数数据格式转换
        point_list = eval(unit.point)
        month_index = int(date.split('-')[1]) - 1
        point_list[month_index] += content_level.point
        unit.point = str(point_list)

        db.session.add(content)
        db.session.commit()
        if content.id is not None:
            flash(f'您已成功添加第{content.id}条数据')
        return redirect(url_for('admin.content_add'))


# 问题信息删除页面
class DelView(MethodView):
    @staticmethod
    @login_required
    @is_admin
    def get(id=None):
        del_con = Content.query.filter_by(id=id).first()
        db.session.delete(del_con)
        db.session.commit()
        flash('信息删除成功')
        return redirect(url_for('admin.content_detail'))


# 问题信息修改页面
class UpdateView(MethodView):
    @staticmethod
    @login_required
    @is_admin
    def post():
        content_id = request.form['id']
        date = request.form['modificationdate']
        state = 2 if request.form['modificationstate'] == 'on' else 0
        edit_con = Content.query.filter_by(id=content_id).first()
        edit_con.modificationstate = state
        edit_con.modificationdate = date
        db.session.commit()
        flash('信息修改成功')
        return redirect(request.referrer)


# 问题列表导出
class ExportView(MethodView):
    @staticmethod
    @login_required
    @is_admin
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
                               content.category2.category, content.case, content.date, content.modificationstate,
                               content.modificationdate]
                worksheet.write_row(i + 1, 0, lst_content)
        workbook.close()
        out.seek(0)
        file_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + "数据.xlsx"
        res = send_file(out, as_attachment=True, attachment_filename=file_name)
        return res


# 文档上传页面
class DocumentUploadOrEdit(MethodView):
    @staticmethod
    @login_required
    @is_admin
    def get(id=None):
        document = Document() if not id else Document.query.filter_by(id=id).first()
        form = DocumentForm(request.form, obj=document)
        form.ftid.choices = [(ft.id, ft.typename) for ft in Filetype.query.all()]
        return render_template('admin/document_edit.html', form=form)

    @staticmethod
    @login_required
    @is_admin
    def post(id=None):
        form = DocumentForm(request.form)
        document = Document() if not id else Document.query.filter_by(id=id).first()

        # for i in form:
        #     print(i)
        form.populate_obj(document)
        print(document)
        # 获取文件名
        file_name = request.files['file'].filename
        if document.filepath is None:
            document.filepath = os.path.join(UPLOAD_FOLDER, file_name)
            if not id:
                db.session.add(document)
            db.session.commit()
            print(document)
        # 保存文件
        file = request.files['file']
        file.save(document.filepath)
        if document.id and not id:
            flash('文档上传成功')
        else:
            flash('文档修改成功')
        return redirect(url_for('admin.document_upload'))


# 文档管理页面
class DocumentDetail(MethodView):
    @staticmethod
    @login_required
    @is_admin
    def get():
        documents = Document.query.all()
        return render_template('admin/document_detail.html', documents=documents)


# 文档删除
class DocumentDelete(MethodView):
    @staticmethod
    @login_required
    @is_admin
    def get(id=None):
        if id:
            document = Document.query.filter_by(id=id).first()
            try:
                os.remove(document.filepath)
                db.session.delete(document)
                db.session.commit()
                flash('文档删除成功')
            except FileNotFoundError:
                flash('文档不存在')
        return redirect(url_for('admin.document_detail'))


# 表扬信息查询页面
class PraiseDetailView(MethodView):
    @staticmethod
    @login_required
    @is_admin
    def get():
        plid = int(request.args.get('praise_level')) if request.args.get('praise_level') else None
        uid = int(request.args.get('unit')) if request.args.get('unit') else None
        c1id = int(request.args.get('category1')) if request.args.get('category1') else None
        page = int(request.args.get('page', 1))
        datefilter = request.args.get('datefilter').split(' - ') if request.args.get('datefilter') else None
        per_page = 10
        if c1id:
            paginate = Praise.query.filter_by(c1id=c1id)
        else:
            paginate = Praise.query.filter_by()
        if plid:
            paginate = paginate.filter_by(plid=plid)
        if uid:
            paginate = paginate.filter_by(uid=uid)
        if datefilter:
            paginate = paginate.filter(Praise.date.between(datefilter[0], datefilter[1]))
        paginate = paginate.paginate(page, per_page)
        category1s = db.session.query(Category1)
        units = Unit.query.all()
        praise_levels = PraiseLevel.query.all()
        return render_template('admin/praise_detail.html', paginate=paginate, category1s=category1s,
                               units=units, praise_levels=praise_levels, uid=uid, c1id=c1id, plid=plid)


# 表扬信息填报页面
class PraiseAddView(MethodView):
    @staticmethod
    @login_required
    @is_admin
    def get():
        category1s = db.session.query(Category1)
        units = Unit.query.all()
        praise_levels = PraiseLevel.query.all()
        return render_template('admin/praise_add.html', category1s=category1s, units=units, praise_levels=praise_levels)

    @staticmethod
    @login_required
    @is_admin
    def post():
        uid = request.form['unit']
        c1id = request.form['category1']
        plid = request.form['praise_level']
        date = request.form['date']
        case = request.form['case']
        filepath = request.form['pics']
        praise = Praise(case, c1id, uid, plid, date, filepath)
        unit = Unit.query.filter_by(id=uid).first()
        praise_level = PraiseLevel.query.filter_by(id=plid).first()

        # 分数数据格式转换
        point_list = eval(unit.point)
        month_index = int(date.split('-')[1]) - 1
        point_list[month_index] += praise_level.point
        unit.point = str(point_list)

        db.session.add(praise)
        db.session.commit()
        if praise.id is not None:
            flash(f'您已成功添加第{praise.id}条数据')
        return redirect(url_for('admin.praise_add'))


class PraiseDelView(MethodView):
    @staticmethod
    @login_required
    @is_admin
    def get(id=None):
        del_praise = Praise.query.filter_by(id=id).first()
        db.session.delete(del_praise)
        db.session.commit()
        flash('信息删除成功')
        return redirect(url_for('admin.praise_detail'))


# 问题管理URL
admin.add_url_rule('add/', view_func=AddView.as_view('content_add'))
admin.add_url_rule('del/<int:id>/', view_func=DelView.as_view('content_delete'))
admin.add_url_rule('detail/', view_func=DetailView.as_view('content_detail'))
admin.add_url_rule('edit/', view_func=UpdateView.as_view('content_edit'))
admin.add_url_rule('detail/export/', view_func=ExportView.as_view('export_data'))
# 文件管理URL
admin.add_url_rule('document_upload/', view_func=DocumentUploadOrEdit.as_view('document_upload'))
admin.add_url_rule('document_edit/<int:id>', view_func=DocumentUploadOrEdit.as_view('document_edit'))
admin.add_url_rule('document_detail/', view_func=DocumentDetail.as_view('document_detail'))
admin.add_url_rule('document_delete/<int:id>', view_func=DocumentDelete.as_view('document_delete'))
# 表扬管理URL
admin.add_url_rule('praise_detail/', view_func=PraiseDetailView.as_view('praise_detail'))
admin.add_url_rule('praise_add/', view_func=PraiseAddView.as_view('praise_add'))
admin.add_url_rule('praise_del/<int:id>/', view_func=PraiseDelView.as_view('praise_delete'))
