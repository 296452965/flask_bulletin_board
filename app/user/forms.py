from flask_wtf import Form
import wtforms


class PasswordForm(Form):
    username = wtforms.StringField('用户名')
    password = wtforms.PasswordField('新密码')
    password2 = wtforms.PasswordField('密码确认')
