from flask import Blueprint, session, redirect, render_template, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user
from flask.views import MethodView
import os

from app.admin.models import *
from config import UPLOAD_FOLDER
from . import user


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


# 信息填报页面
class BadgeInfoView(MethodView):
    @staticmethod
    @login_required
    def get():
        return render_template('user/badge.html')

    @staticmethod
    @login_required
    def post():
        dict_data = request.form.to_dict()
        print(dict_data)

        # 小章章暂存队列
        badge_list = []
        # 注意事项暂存队列
        info_list = []

        # 1.确定岗级
        if dict_data['level']:
            badge_list.append(dict_data['level'])
            info_list.append('')

        # 2.确定工作年限小章章组合
        work_years = int(dict_data['year'])
        year_list = []
        year_info_list = []
        decade = work_years // 10
        years = work_years % 10
        if decade:
            year_list.append(str(175 + decade))
            year_info_list.append('')
            if years:
                year_list.append(str(166 + years))
                year_info_list.append('')
        else:
            year_list.append(str(166 + years))
            year_info_list.append('')
        print('year_list: ', year_list)

        # 荣誉类
        # 3.确定第1块小章章 red
        list_1 = []
        info_list_1 = []
        for i in range(1, 31):
            if dict_data[str(i)]:
                for j in range(int(dict_data[str(i)])):
                    list_1.append(str(i))
                    info_list_1.append('')
        print('list_1: ', list_1)

        # 4.确定第2块小章章 orange/orange+yellow+2
        list_2 = []
        info_list_2 = []
        for i in range(31, 52):
            if dict_data[str(i)]:
                list_2.append(str(i))
                info_list_2.append('(次数用数字配件)')
        print('list_2: ', list_2)

        # 5.确定第3块小章章 green+1+2
        list_3 = []
        info_list_3 = []
        for i in range(52, 56):
            if dict_data[str(i)]:
                list_3.append(str(i))
                info_list_3.append('(随机选择一种情形)')
                break
        print('list_3: ', list_3)

        # 6.确定第4块小章章 green+2
        list_4 = []
        info_list_4 = []
        for i in range(56, 59):
            if dict_data[str(i)]:
                list_4.append(str(i))
                info_list_4.append('(次数用数字配件)')
        print('list_4: ', list_4)

        # 7.确定第5块小章章 green+2+3--3级选最高级
        list_5 = []
        info_list_5 = []
        for i in range(59, 68, 3):
            for j in range(i, i + 3):
                if dict_data[str(j)]:
                    list_5.append(str(j))
                    info_list_5.append('(次数用数字配件)')
                    break
        print('list_5: ', list_5)

        # 8.确定第6块小章章 red
        list_6 = []
        info_list_6 = []
        for i in range(68, 70):
            if dict_data[str(i)]:
                for j in range(int(dict_data[str(i)])):
                    list_6.append(str(i))
                    info_list_6.append('')
        print('list_6: ', list_6)

        # 9.确定第7块小章章 green+2+3--3级选最高级
        list_7 = []
        info_list_7 = []
        for i in range(70, 91, 3):
            for j in range(i, i + 3):
                if dict_data[str(j)]:
                    list_7.append(str(j))
                    info_list_7.append('(次数用数字配件)')
                    break
        print('list_7: ', list_7)

        # 经历类
        # 10.确定第8块小章章 red
        list_8 = []
        info_list_8 = []
        for i in range(91, 92):
            if dict_data[str(i)]:
                for j in range(int(dict_data[str(i)])):
                    list_8.append(str(i))
                    info_list_8.append('')
        print('list_8: ', list_8)

        # 11.确定第9块小章章 green+2
        list_9 = []
        info_list_9 = []
        for i in range(92, 94):
            if dict_data[str(i)]:
                list_9.append(str(i))
                info_list_9.append('(次数用数字配件)')
        print('list_9: ', list_9)

        # 12.确定第10块小章章 green+2+3--3级选最高级
        list_10 = []
        info_list_10 = []
        for i in range(94, 100, 3):
            for j in range(i, i + 3):
                if dict_data[str(j)]:
                    list_10.append(str(j))
                    info_list_10.append('(次数用数字配件)')
                    break
        print('list_10: ', list_10)

        # 13.确定第11块小章章 orange+4/orange+4+9
        list_11 = []
        info_list_11 = []
        for i in range(100, 119):
            if dict_data[str(i)]:
                if i in (100, 116):  # 如果输入类别33，需要提示佩戴方式9
                    list_11.append(str(i))
                    info_list_11.append('(选择该层级最高职务)')
                else:
                    list_11.append(str(i))
                    info_list_11.append('')
        print('list_11: ', list_11)

        # 14.确定第12块小章章 yellow+7+8/yellow
        list_12 = []
        info_list_12 = []
        for i in range(119, 127):
            if dict_data[str(i)]:
                list_12.append(str(i))
                info_list_12.append('(按任职顺序排列，现任职不佩戴)')
        for i in range(127, 129):
            if dict_data[str(i)]:
                list_12.append(str(i))
                info_list_12.append('')
        print('list_12: ', list_12)

        # 15.确定第13块小章章 green+3--4级选最高级
        list_13 = []
        info_list_13 = []
        for i in range(129, 133):
            if dict_data[str(i)]:
                list_13.append(str(i))
                info_list_13.append('')
                break
        print('list_13: ', list_13)

        # 16.确定第14块小章章 orange+4
        list_14 = []
        info_list_14 = []
        for i in range(133, 142):
            if dict_data[str(i)]:
                list_14.append(str(i))
                info_list_14.append('')
        print('list_14: ', list_14)

        # 17.确定第15块小章章 green+2
        list_15 = []
        info_list_15 = []
        for i in range(142, 143):
            if dict_data[str(i)]:
                list_15.append(str(i))
                info_list_13.append('(次数用数字配件)')
        print('list_15: ', list_15)

        for i in range(1, 16):
            badge_list += eval(f'list_{i}')

        for i in range(1, 16):
            info_list += eval(f'info_list_{i}')

        if len(badge_list) + len(year_list) > 21:
            badge_list = badge_list[:-len(year_list)] + year_list
            info_list = info_list[:-len(year_info_list)] + year_info_list
        else:
            badge_list += year_list
            info_list += year_info_list

        print(len(badge_list))
        print(badge_list)
        print(len(info_list))
        print(info_list)
        import math
        from .image_combine import image_compose_1, image_compose_2, image_compose_3
        IMAGE_ROW = math.ceil(len(badge_list) / 3)  # 合并图片行数
        IMAGE_COLUMN = 3  # 合并图片列数
        IMAGE_OF_FIRST_ROW = len(badge_list) % 3  # 第一列图片数

        if IMAGE_OF_FIRST_ROW == 1:
            image_compose_1(IMAGE_ROW, IMAGE_COLUMN, badge_list)
        elif IMAGE_OF_FIRST_ROW == 2:
            image_compose_2(IMAGE_ROW, IMAGE_COLUMN, badge_list)
        elif IMAGE_OF_FIRST_ROW == 3:
            image_compose_3(IMAGE_ROW, IMAGE_COLUMN, badge_list)

        return redirect(url_for('user.badge'))


user.add_url_rule('badge/', view_func=BadgeInfoView.as_view('badge'))
