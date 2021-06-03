from flask import Blueprint
bossinfo = Blueprint('bossinfo', __name__, url_prefix='/v1/bossinfo')

from . import view