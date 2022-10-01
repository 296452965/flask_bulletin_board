from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
import wtforms


class DocumentForm(Form):
    ftid = wtforms.SelectField('文档类型')
    filename = wtforms.StringField('文件名称')
    file = FileField('文件上传', validators=[FileAllowed(['.pdf'], '只能上传PDF文件！'), FileRequired('未选择文件！')])
    submit = wtforms.SubmitField('上传')