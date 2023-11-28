from . import sql 
import pymysql
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('account', __name__, url_prefix='/account')

host = 'localhost'
user = 'root'
dbpassword = '7Sanctuaries!'

@bp.route('/')
def account():
    return 'hello'

@bp.route('/login/',methods=['GET','POST'])
def login():
    '''
    request(POST) data:
        email (or username for staff)
        password
        type - the type of login
    '''
    msg = ''
    if request.method=='POST' and 'password' in request.form:
        password = request.form['password']
        email = request.form['email']
        connection = pymysql.connect(host = host, port = 3307, user = user, password = dbpassword, database = 'air_ticket')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM customer WHERE email = % s AND password = % s', (email, password, ))
        customer = cursor.fetchone()
        if customer:
            session['loggedin'] = True
            session['username'] = customer[1]
            return redirect("/public/home")
        else:
            msg = 'Invalid username or password!'
    return render_template('login.html', msg = msg)

@bp.route('/logout/')
def logout():
    '''
    remove user data from session
    '''
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return 'hello'

@bp.route('/register/',methods=['GET','POST'])
def register():
    '''
    request(POST) data:
        a ton of user data (refer to sql)
        type - the type of user
    '''
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        connection = pymysql.connect(host = host, port = 3307, user = user, password = dbpassword, database = "air_ticket")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    if request.method=='POST':
        print(request.form['type'])
        return redirect("/account/login")
    return render_template('register.html')



