from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('account',__name__,url_prefix='/account')

@bp.route('/')
def account():
    return 'hello'

@bp.route('/login',methods=['GET','POST'])
def login():
    '''
    request(POST) data:
        email (or username for staff)
        password
        type - the type of login
    '''
    if request.method=='POST':
        print(request.form['type'])
        return redirect("/public/home")
    return render_template('login.html')

@bp.route('/logout')
def logout():
    '''
    remove user data from session
    '''
    return 'hello'

@bp.route('/register',methods=['GET','POST'])
def register():
    '''
    request(POST) data:
        a ton of user data (refer to sql)
        type - the type of user
    '''
    if request.method=='POST':
        print(request.form['type'])
        return redirect("/account/login")
    return render_template('register.html')



