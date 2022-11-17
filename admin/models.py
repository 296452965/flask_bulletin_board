# flask-sqlalchemy的基本使用
from exts import db


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
    department = db.relationship('Department', back_populates='unit')

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
        return "<Category1(id='%s',category='%s')>" % (self.id, self.category)


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
        return "<Category2(id='%s',category='%s',c1id='%s)>" % (self.id, self.category, self.c1id)


# 情况登记表，问题，问题类型编号，单位编号，发生时间
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    problem = db.Column(db.Text)
    c1id = db.Column(db.Integer, db.ForeignKey('category1.id'))
    c2id = db.Column(db.Integer, db.ForeignKey('category2.id'))
    uid = db.Column(db.Integer, db.ForeignKey('unit.id'))
    date = db.Column(db.Date)
    modificationstate = db.Column(db.SmallInteger)  # 0 未整改 1 整改待确认 2 已整改
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
               % (self.id, self.problem, self.c1id, self.c2id, self.uid, self.date, self.modificationstate,
                  self.modificationdate)


# 相关文档表，文档名称，文档路径，文档类型
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(100))
    filepath = db.Column(db.String(100))
    ftid = db.Column(db.Integer, db.ForeignKey('filetype.id'))
    filetype = db.relationship('Filetype', back_populates='documents')

    def __init__(self, filename=None, filepath=None, ftid=None):
        self.filename = filename
        self.filepath = filepath
        self.ftid = ftid

    def __repr__(self):
        return "<Document(id='%s',filename='%s',filepath='%s',ftid='%s')>" % \
               (self.id, self.filename, self.filepath, self.ftid)


# 相关文档分类
class Filetype(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    typename = db.Column(db.String(50))
    documents = db.relationship('Document', back_populates='filetype')

    def __init__(self, typename):
        self.typename = typename

    def __repr__(self):
        return "<Filetype(id='%s', filetype='%s')>" % (self.id, self.typename)


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    badge_name = db.Column(db.String(50))
    pic_path = db.Column(db.String(100))
    detail = db.Column(db.String(128))
    same_badge_can_be_worn_concurrently = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer)
    same_level_can_be_worn_concurrently = db.Column(db.Integer)
    condition = db.Column(db.String(32))
    different_condition_can_be_worn_concurrently = db.Column(db.Integer)
    num_can_be_worn = db.Column(db.Integer)
    wearing_method_1 = db.Column(db.Integer)
    wearing_method_2 = db.Column(db.Integer)
    priority = db.Column(db.Integer)
    bt_id = db.Column(db.Integer, db.ForeignKey('badgetype.id'))
    badgetype = db.relationship('BadgeType', back_populates='badges')

    def __init__(self, badge_name=None, pic_path=None, detail=None, same_badge_can_be_worn_concurrently=None,
                 level=None, same_level_can_be_worn_concurrently=None, condition=None,
                 different_condition_can_be_worn_concurrently=None, num_can_be_worn=None, wearing_method_1=None,
                 wearing_method_2=None, priority=None, bt_id=None):
        self.badge_name = badge_name
        self.pic_path = pic_path
        self.detail = detail
        self.same_badge_can_be_worn_concurrently = same_badge_can_be_worn_concurrently
        self.level = level
        self.same_level_can_be_worn_concurrently = same_level_can_be_worn_concurrently
        self.condition = condition
        self.different_condition_can_be_worn_concurrently = different_condition_can_be_worn_concurrently
        self.num_can_be_worn = num_can_be_worn
        self.wearing_method_1 = wearing_method_1
        self.wearing_method_2 = wearing_method_2
        self.priority = priority
        self.bt_id = bt_id


class BadgeType(db.Model):
    __tablename__ = 'badgetype'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_1_name = db.Column(db.String(50))  # 大类
    cat_2_name = db.Column(db.String(50))  # 类
    typename = db.Column(db.String(50))  # 项目名称
    badges = db.relationship('Badge', back_populates='badgetype')

    def __init__(self, cat_1_name, cat_2_name, typename):
        self.cat_1_name = cat_1_name
        self.cat_2_name = cat_2_name
        self.typename = typename
