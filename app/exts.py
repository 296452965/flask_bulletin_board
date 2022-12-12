from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import os
ALLOWED_EXTENTIONS = ['.jpg', '.png', '.gif']


# 检查文件是否允许上传
def allowed_file(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENTIONS
