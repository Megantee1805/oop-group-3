import functools
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from foodhubsg.db import *

support = 'support@foodhub.sg'
support_password = generate_password_hash('Iamasupport')
g.user['name'] = 'Support'

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/support_index')
def suppprt():
    return render_template('support/support_index.html')
