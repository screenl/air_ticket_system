from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('account',__name__,url_prefix='/account')

@bp.route('/')
def account():
    return 'hello'

@bp.route('/login')
def login():
    return 'hello'

@bp.route('/register')
def register():
    return render_template('register.html')

@bp.route('/register_customer',methods=['POST'])
def register_customer():
    '''
    handle customer registration
    '''
    return ''

@bp.route('/register_agent',methods=['POST'])
def register_agent():
    return ''

@bp.route('/register_staff',methods=['POST'])
def register_staff():
    return ''

@bp.route('/auth',methods=['POST'])
def auth():
    return ''

