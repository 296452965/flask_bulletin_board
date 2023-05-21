from flask import Blueprint

department = Blueprint('department', __name__, url_prefix='/department/')

from .views import *
