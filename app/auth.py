from flask import (Blueprint, flash, redirect, url_for)
from .models import *

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    user1 = Radcheck.query.where(Radcheck.id > 1).first()
    return f"<h1>Coucouu {user1.username}</h1>"