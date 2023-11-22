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
    if request.method=='POST':
        print(request.form['type'])
        return redirect("/public/home")
    return render_template('login.html')

@bp.route('/logout')
def logout():
    return 'hello'

@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        print(request.form['type'])
        return redirect("/account/login")
    return render_template('register.html')



