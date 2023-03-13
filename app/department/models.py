from app.admin.models import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
db = db  # 赋值给一变量，否则系统会只找到admin应用的db


class Department(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    uid = db.Column(db.Integer, db.ForeignKey('unit.id'))
    u2id = db.Column(db.Integer, db.ForeignKey('unit2.id'))
    rid = db.Column(db.Integer, db.ForeignKey('role.id'))
    unit = db.relationship('Unit', back_populates='department')
    unit2 = db.relationship('Unit2', back_populates='departments')
    role = db.relationship('Role', back_populates='departments')

    def __init__(self, username=None, uid=None, u2id=None, rid=None):
        self.username = username
        self.uid = uid
        self.u2id = u2id
        self.rid = rid

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# TODO 角色权限
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50))
    # 数据权限总值
    data_permission = db.Column(db.Integer)
    # 页面权限总值
    page_permission = db.Column(db.Integer)
    departments = db.relationship('Department', back_populates='role')

    def __init__(self, role_name, data_permission, page_permission):
        self.role_name = role_name
        self.data_permission = data_permission
        self.page_permission = page_permission

    def __repr__(self):
        return "<Role(id='%s',role_name='%s',data_permission='%s',page_permission='%s')>" % (self.id, self.role_name,
                                                                                             self.data_permission,
                                                                                             self.data_permission)


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 权限名
    permission_name = db.Column(db.String(50))
    # 权限值
    permission_value = db.Column(db.Integer)

    def __init__(self, permission_name, permission_value):
        self.permission_name = permission_name
        self.permission_value = permission_value

    def __repr__(self):
        return "<Permission(id='%s',permission_name='%s',permission_value='%s')>" % (self.id, self.permission_name,
                                                                                     self.permission_value)

