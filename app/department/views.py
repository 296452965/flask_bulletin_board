from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.views import MethodView
from flask_login import login_required

from .forms import DepartmentForm
from .models import Department, db
from . import department
from app.admin.models import Unit
from app.decorators import is_admin


# 部门详情
@department.route('detail/')
@login_required
@is_admin
def detail():
    departments = Department.query.all()
    return render_template('admin/department_detail.html', departments=departments)


# 部门编辑
class DepartmentCreatOrEdit(MethodView):
    @staticmethod
    @login_required
    @is_admin
    def get(id=None):
        department = Department() if not id else Department.query.filter_by(id=id).first()
        form = DepartmentForm(request.form, obj=department)
        form.uid.choices = [(u.id, u.unit_name) for u in Unit.query.all()]
        return render_template('admin/department_edit.html', form=form)

    @staticmethod
    @login_required
    @is_admin
    def post(id=None):
        print(request.form)
        form = DepartmentForm(formdata=request.form)
        print(form)
        department = Department() if not id else Department.query.filter_by(id=id).first()
        form.populate_obj(department)
        department.set_password(form.password.data)
        if not id:
            db.session.add(department)
        db.session.commit()
        if department.id and not id:
            flash('信息添加成功')
        else:
            flash('信息修改成功')
        return redirect(url_for('department.detail'))


# 部门删除
class DepartmentDelete(MethodView):
    @staticmethod
    @login_required
    @is_admin
    def get(id=None):
        if id:
            department = Department.query.filter_by(id=id).first()
            db.session.delete(department)
            db.session.commit()
            flash('信息删除成功')
        return redirect(url_for('department.detail'))


department.add_url_rule('edit/<int:id>', view_func=DepartmentCreatOrEdit.as_view('edit'))
department.add_url_rule('create/', view_func=DepartmentCreatOrEdit.as_view('create'))
department.add_url_rule('delete/<int:id>', view_func=DepartmentDelete.as_view('delete'))
