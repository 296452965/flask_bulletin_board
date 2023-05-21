from flask_wtf import Form
import wtforms


class DepartmentForm(Form):
    uid = wtforms.SelectField('单位')
    rid = wtforms.SelectField('角色', choices=[(1, '用户'), (2, '管理员')], coerce=int)
    username = wtforms.StringField('用户名')
    password = wtforms.StringField('密码')
