from flask import Blueprint

department = Blueprint('department', __name__, url_prefix='/')

from .views import *
