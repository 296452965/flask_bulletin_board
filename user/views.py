from flask import Blueprint, session, redirect, render_template, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user
import os

from admin.models import *
from settings import UPLOAD_FOLDER

user = Blueprint('user', __name__, url_prefix='/user/')


# 用户页面主页
@user.route('index/')
@login_required
def index():
    uid = current_user.uid
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
        Document.filename.like('%'+search_key+'%') if search_key else Document.filename.like('%%')
    ).all()
    return render_template('user/inform.html', documents=documents)


# 政策页面
@user.route('policy/')
@login_required
def policy():
    search_key = request.args.get('search_key', '')
    documents = Document.query.filter_by(ftid=2).filter(
        Document.filename.like('%'+search_key+'%') if search_key else Document.filename.like('%%')
    ).all()
    return render_template('user/policy.html', documents=documents)


# 案例页面
@user.route('case/')
@login_required
def case():
    search_key = request.args.get('search_key', '')
    documents = Document.query.filter_by(ftid=3).filter(
        Document.filename.like('%'+search_key+'%') if search_key else Document.filename.like('%%')
    ).all()
    return render_template('user/case.html', documents=documents)


# 视频页面
@user.route('video/')
@login_required
def video():
    documents = Document.query.filter_by(ftid=4).all()
    return render_template('user/video.html', documents=documents)


@user.route('document/download/<int:fid>')
@login_required
def document_download(fid):
    file = Document.query.filter_by(id=fid).first()
    file_path = file.filepath
    name = file_path.split('\\')[-1]  # 切割出文件名称
    path = file_path.replace(name, '')
    res = send_from_directory(path, filename=name, as_attachment=True)
    return res


@user.route('video/watch/<int:fid>')
@login_required
def video_watch(fid):
    file = Document.query.filter_by(id=fid).first()
    file_path = file.filepath
    path, filename = os.path.split(file_path)
    return render_template('user/video_watch.html', filename=filename)


# Ajax提交整改待确认
@user.route('change_state')
def change_state():
    id = request.args.get('id')
    content = Content.query.filter_by(id=id).first()
    content.modificationstate = 1
    db.session.commit()
    return redirect(url_for('user.index'))


# 呈现特定目录下的资源
@user.route('/document/<filename>/')
def render_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return '该文件不存在'
