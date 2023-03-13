# flask-sqlalchemy的基本使用
# db的引用关系: exts<-admin<-department
from app.exts import db


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


# 二级单位名称映射表
class Unit2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(50))
    contents = db.relationship('Content', back_populates='unit2')
    praises = db.relationship('Praise', back_populates='unit2')
    departments = db.relationship('Department', back_populates='unit2')
    units = db.relationship('Unit', back_populates='unit2')

    def __int__(self, unit_name):
        self.unit_name = unit_name

    def __repr__(self):
        return "<Unit2(id='%s', unit_name='%s')>" % (self.id, self.unit_name)


# 本机单位名称映射表, u2id:所属二级单位id
class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(50))
    point = db.Column(db.String(100), default='[80,80,80,80,80,80,80,80,80,80,80,80]')
    u2id = db.Column(db.Integer, db.ForeignKey('unit2.id'))
    contents = db.relationship('Content', back_populates='unit')
    praises = db.relationship('Praise', back_populates='unit')
    department = db.relationship('Department', back_populates='unit')
    unit2 = db.relationship('Unit2', back_populates='units')

    def __init__(self, unit_name, point, u2id):
        self.unit_name = unit_name
        self.point = point
        self.u2id = u2id

    def __repr__(self):
        return "<Unit(id='%s',unit_name='%s',u2id='%s')>" % (self.id, self.unit_name, self.u2id)


# 问题分级映射表
class ContentLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String(50))
    point = db.Column(db.Float)
    contents = db.relationship('Content', back_populates='content_level')

    def __init__(self, level_name, point):
        self.level_name = level_name
        self.point = point

    def __repr__(self):
        return "<ContentLevel(id='%s',level_name='%s',point='%s')>" % (self.id, self.level_name, self.point)


# 表扬分级映射表
class PraiseLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String(50))
    point = db.Column(db.Float)
    praises = db.relationship('Praise', back_populates='praise_level')

    def __init__(self, level_name, point):
        self.level_name = level_name
        self.point = point

    def __repr__(self):
        return "<PraiseLevel(id='%s',level_name='%s',point='%s')>" % (self.id, self.level_name, self.point)


# 情况（表扬、问题）一级分类映射表
class Category1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    contents = db.relationship('Content', back_populates='category1')
    praises = db.relationship('Praise', back_populates='category1')
    category2s = db.relationship('Category2', back_populates='category1')

    def __init__(self, category):
        self.category = category

    def __repr__(self):
        return "<Category1(id='%s',category='%s')>" % (self.id, self.category)


# 情况（表扬、问题）二级分类映射表，细化分类
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


# 情况登记表，问题，问题类型编号，单位编号，发生日期，整改状态，整改日期，图片路径
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case = db.Column(db.Text)
    c1id = db.Column(db.Integer, db.ForeignKey('category1.id'))
    c2id = db.Column(db.Integer, db.ForeignKey('category2.id'))
    uid = db.Column(db.Integer, db.ForeignKey('unit.id'))
    u2id = db.Column(db.Integer, db.ForeignKey('unit2.id'))
    clid = db.Column(db.Integer, db.ForeignKey('content_level.id'))
    date = db.Column(db.Date)
    modification_state = db.Column(db.SmallInteger)  # 0 未整改 1 整改待确认 2 已整改
    modification_date = db.Column(db.Date)
    filepath = db.Column(db.String(256))
    category1 = db.relationship('Category1', back_populates='contents')
    category2 = db.relationship('Category2', back_populates='contents')
    unit = db.relationship('Unit', back_populates='contents')
    unit2 = db.relationship('Unit2', back_populates='contents')
    content_level = db.relationship('ContentLevel', back_populates='contents')

    def __init__(self, case, c1id, c2id, uid, u2id, clid, date, modification_state, modification_date, filepath):
        self.case = case
        self.c1id = c1id
        self.c2id = c2id
        self.uid = uid
        self.u2id = u2id
        self.date = date
        self.clid = clid
        self.modification_state = modification_state
        self.modification_date = modification_date
        self.filepath = filepath

    def __repr__(self):
        return "<Content(id='%s',case='%s',c1id='%s',c2id='%s',uid='%s',u2id='%s',clid='%s',date='%s',\
                modification_state='%s',modification_date='%s')>" % \
               (self.id, self.case, self.c1id, self.c2id, self.uid, self.u2id, self.clid, self.date,
                self.modification_state, self.modification_date)


# 表扬登记表，情况，情况类型编号，单位编号，发生日期，图片路径
class Praise(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case = db.Column(db.Text)
    c1id = db.Column(db.Integer, db.ForeignKey('category1.id'))
    uid = db.Column(db.Integer, db.ForeignKey('unit.id'))
    u2id = db.Column(db.Integer, db.ForeignKey('unit2.id'))
    plid = db.Column(db.Integer, db.ForeignKey('praise_level.id'))
    date = db.Column(db.Date)
    filepath = db.Column(db.String(256))
    category1 = db.relationship('Category1', back_populates='praises')
    unit = db.relationship('Unit', back_populates='praises')
    unit2 = db.relationship('Unit2', back_populates='praises')
    praise_level = db.relationship('PraiseLevel', back_populates='praises')

    def __init__(self, case, c1id, uid, u2id, plid, date, filepath):
        self.case = case
        self.c1id = c1id
        self.uid = uid
        self.u2id = u2id
        self.plid = plid
        self.date = date
        self.filepath = filepath

    def __repr__(self):
        return "<Praise(id='%s',case='%s',c1id='%s',uid='%s',u2id='%s',plid='%s',date='%s')>" \
               % (self.id, self.case, self.c1id, self.uid, self.u2id, self.plid, self.date)


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


# 奖章信息表
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


# 奖章分类表
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


