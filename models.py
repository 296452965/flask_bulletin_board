# flask-sqlalchemy的基本使用
from exts import db


# 管理员信息表
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<Admin(id='%s',username='%s',password='%s')>" % (self.id, self.username, self.password)


# 用户信息表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # name字段，字符类型，最大的长度是50个字符
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # 让打印出来的数据更好看，可选的
    def __repr__(self):
        return "<User(id='%s',username='%s',password='%s')>" % (self.id, self.username, self.password)


# 柱状图数据表
class DataBar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Integer)
    data = db.Column(db.Integer)

    def __init__(self, label, data):
        self.label = label
        self.data = data

    def __repr__(self):
        return "<DataBar(id='%s',label='%s',data='%s')>" % (self.id, self.label, self.data)


# 线状图数据表
class DataLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Integer)
    data = db.Column(db.Integer)

    def __init__(self, label, data):
        self.label = label
        self.data = data

    def __repr__(self):
        return "<DataLine(id='%s',label='%s',data='%s')>" % (self.id, self.label, self.data)


# 单位名称映射表
class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unitname = db.Column(db.String(50))
    contents = db.relationship('Content', back_populates='unit')

    def __init__(self, unitname):
        self.unitname = unitname

    def __repr__(self):
        return "<Unit(id='%s',unitname='%s')>" % (self.id, self.unitname)


# 问题一级分类映射表
class Category1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    contents = db.relationship('Content', back_populates='category1')
    category2s = db.relationship('Category2', back_populates='category1')

    def __init__(self, category):
        self.category = category

    def __repr__(self):
        return "<Unit(id='%s',category='%s')>" % (self.id, self.category)


# 问题二级分类映射表，细化分类
class Category2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    c1id = db.Column(db.Integer, db.ForeignKey('category1.id'))
    contents = db.relationship('Content', back_populates='category2')
    category1 = db.relationship('Category1', back_populates='category2s')

    def __init__(self, category, c1id):
        self.category = category
        self.c1id = c1id

    def __repr__(self):
        return "<Unit(id='%s',category='%s',c1id='%s)>" % (self.id, self.category, self.c1id)


# 情况登记表，问题，问题类型编号，单位编号，发生时间
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem = db.Column(db.Text)
    c1id = db.Column(db.Integer, db.ForeignKey('category1.id'))
    c2id = db.Column(db.Integer, db.ForeignKey('category2.id'))
    uid = db.Column(db.Integer, db.ForeignKey('unit.id'))
    date = db.Column(db.Date)
    modificationstate = db.Column(db.Boolean)
    modificationdate = db.Column(db.Date)
    category1 = db.relationship('Category1', back_populates='contents')
    category2 = db.relationship('Category2', back_populates='contents')
    unit = db.relationship('Unit', back_populates='contents')

    def __init__(self, problem, c1id, c2id, uid, date, modificationstate, modificationdate):
        self.problem = problem
        self.c1id = c1id
        self.c2id = c2id
        self.uid = uid
        self.date = date
        self.modificationstate = modificationstate
        self.modificationdate = modificationdate

    def __repr__(self):
        return "<Content(id='%s',problem='%s',c1id='%s',c2id='%s',uid='%s',date='%s'),modificationstate='%s',modificationdate='%s'>" \
               % (self.id, self.problem, self.c1id, self.c2id, self.uid, self.date, self.modificationstate, self.modificationdate)


# db.create_all()
# admin = Admin('admin', '123456')
# user = User('user', '123456')
# unit = Unit('单位一')
# db.session.add(admin)
# db.session.add(user)
# db.session.add(unit)
# db.session.commit()
