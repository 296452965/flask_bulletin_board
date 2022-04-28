from admin.models import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
db = db  # 赋值给一变量，否则系统会只找到admin应用的db


class Department(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    uid = db.Column(db.Integer, db.ForeignKey('unit.id'))
    role = db.Column(db.Integer)
    unit = db.relationship('Unit', back_populates='department')

    def __init__(self, username=None, uid=None, role=None):
        self.username = username
        self.uid = uid
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
