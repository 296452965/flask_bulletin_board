from flask import session, redirect, render_template, url_for, flash, request, send_from_directory
from flask.views import MethodView
from flask_login import login_required, current_user
import os

from app.admin.models import *
from app.department.models import *
from config import UPLOAD_FOLDER
from . import user
from .forms import PasswordForm


# 用户页面主页
@user.route('index/')
@login_required
def index():
    uid = current_user.uid
    u2id = current_user.u2id
    print('uid:',uid)
    print('u2id:',u2id)
    per_page = 10
    page = int(request.args.get('page', 1))
    contents = Content.query.filter_by(uid=uid).paginate(page, per_page)
    return render_template('user/index.html', contents=contents)


# 个人信息编辑页面
@user.route('profile/')
@login_required
def profile():
    return render_template('user/profile.html')


# 通知页面
@user.route('inform/')
@login_required
def inform():
    search_key = request.args.get('search_key', '')
    documents = Document.query.filter_by(ftid=1).filter(
        Document.filename.like('%' + search_key + '%') if search_key else Document.filename.like('%%')
    ).all()
    return render_template('user/inform.html', documents=documents)


# 政策页面
@user.route('policy/')
@login_required
def policy():
    search_key = request.args.get('search_key', '')
    documents = Document.query.filter_by(ftid=2).filter(
        Document.filename.like('%' + search_key + '%') if search_key else Document.filename.like('%%')
    ).all()
    return render_template('user/policy.html', documents=documents)


# 案例页面
@user.route('case/')
@login_required
def case():
    search_key = request.args.get('search_key', '')
    documents = Document.query.filter_by(ftid=3).filter(
        Document.filename.like('%' + search_key + '%') if search_key else Document.filename.like('%%')
    ).all()
    return render_template('user/case.html', documents=documents)


# 视频页面
@user.route('video/')
@login_required
def video():
    documents = Document.query.filter_by(ftid=4).all()
    return render_template('user/video.html', documents=documents)


# 下载文件
@user.route('document/download/<int:fid>')
@login_required
def document_download(fid):
    file = Document.query.filter_by(id=fid).first()
    file_path = file.filepath
    name = file_path.split('\\')[-1]  # 切割出文件名称
    path = file_path.replace(name, '')
    res = send_from_directory(path, filename=name, as_attachment=True)
    return res


# 观看视频
@user.route('video/watch/<int:fid>')
@login_required
def video_watch(fid):
    file = Document.query.filter_by(id=fid).first()
    file_path = file.filepath
    path, filename = os.path.split(file_path)
    return render_template('user/video_watch.html', filename=filename)


# 提交整改待确认
@user.route('change_state')
@login_required
def change_state():
    id = request.args.get('id')
    content = Content.query.filter_by(id=id).first()
    content.modification_state = 1
    db.session.commit()
    return redirect(url_for('user.index'))


# 呈现特定目录下的资源
@user.route('/document/<filename>/')
@login_required
def render_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return '该文件不存在'


# 密码修改
@user.route('password_edit/', methods=['GET','POST'])
@login_required
def password_edit():
    username = session.get('username')
    department = Department.query.filter_by(username=username).first()
    if request.method == 'POST':
        form = PasswordForm(request.form)
        if form.password.data != form.password2.data:
            flash('两次密码不一致')
            return redirect(url_for('user.password_edit'))
        department.set_password(form.password.data)
        db.session.commit()
        flash('密码修改成功，重新登录')
        return redirect(url_for('login.logout'))
    form = PasswordForm(request.form, obj=department)
    return render_template('user/password_edit.html', form=form)


# 类视图(CBV)
# 问题信息查询页面
class DetailView(MethodView):
    @staticmethod
    @login_required
    def get():
        clid = int(request.args.get('content_level')) if request.args.get('content_level') else None
        uid = current_user.uid
        c1id = int(request.args.get('category1')) if request.args.get('category1') else None
        c2id = int(request.args.get('category2')) if request.args.get('category2') else None
        modification_state = int(request.args.get('modification_state')) if request.args.get('modification_state') else None
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
        if modification_state is not None:
            paginate = paginate.filter_by(modification_state=modification_state)
        # 根据是否选择日期范围确定过滤方式
        if datefilter:
            paginate = paginate.filter(Content.date.between(datefilter[0], datefilter[1]))
        paginate = paginate.paginate(page, per_page)
        category1s = db.session.query(Category1)
        units = Unit.query.all()
        content_levels = ContentLevel.query.all()
        return render_template('user/content_detail.html', paginate=paginate, category1s=category1s,
                               units=units, content_levels=content_levels, c1id=c1id, c2id=c2id, clid=clid)


# 表扬信息查询页面
class PraiseDetailView(MethodView):
    @staticmethod
    @login_required
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
        return render_template('user/praise_detail.html', paginate=paginate, category1s=category1s,
                               units=units, praise_levels=praise_levels, uid=uid, c1id=c1id, plid=plid)


user.add_url_rule('detail/', view_func=DetailView.as_view('content_detail'))
user.add_url_rule('praise_detail/', view_func=PraiseDetailView.as_view('praise_detail'))