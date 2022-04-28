from flask_wtf import Form
import wtforms


class DepartmentForm(Form):
    uid = wtforms.SelectField('单位')
    role = wtforms.SelectField('角色', choices=[('0', '用户'), ('1', '管理员')])
    username = wtforms.StringField('用户名')
    password = wtforms.StringField('密码')
