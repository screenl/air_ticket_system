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
    if request.method=='POST' and 'password' in request.form:
        type = request.form["type"]
        password = request.form['password']
        if type != 'staff':
            email = request.form['email']
        else:
            username = request.form['username']
        connection = pymysql.connect(host = host, port = 3307, user = user, password = dbpassword, database = 'air_ticket')
        cursor = connection.cursor()
        #print('SELECT * FROM % s WHERE email = % s AND password = % s', (type, email, password, ))
        if type == 'customer':
            cursor.execute('SELECT * FROM customer WHERE email = % s AND password = % s', (email, password, ))
        elif type == 'agent':
            cursor.execute('SELECT * FROM agent WHERE agent_email = % s AND password = % s', (email, password, ))
        elif type == 'staff':
            cursor.execute('SELECT * FROM staff WHERE username = % s AND password = % s', (username, password, ))
        customer = cursor.fetchone()
        print(request)
        if customer:
            session['loggedin'] = True
            session['username'] = customer[1]
            return redirect("/public/home")
        else:
            flash('Invalid username or password!')
    return render_template('login.html')

@bp.route('/logout/')
def logout():
    '''
    remove user data from session
    '''
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for(login))

@bp.route('/register/',methods=['GET','POST'])
def register():
    '''
    request(POST) data:
        a ton of user data (refer to sql)
        type - the type of user
    '''
    if request.method == 'POST':
        type = request.form["type"]
        id = type
        connection = pymysql.connect(host = host, port = 3307, user = user, password = dbpassword, database = "air_ticket")
        cursor = connection.cursor()
        if type == 'customer':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            building_number = request.form['building_number']
            street = request.form["street"]
            city = request.form["city"]
            state = request.form["state"]
            phone_number = request.form["phone_number"]
            passport_number = request.form["passport_number"]
            passport_expiration = request.form["passport_expiration"]
            passport_country = request.form["passport_country"]
            date_of_birth = request.form["date_of_birth"]
            cursor.execute('SELECT * FROM customer WHERE name = % s', (name, ))
            account = cursor.fetchone()
            if account:
                flash('Account already exists !')
            else:
                cursor.execute(
                    'INSERT INTO customer VALUES (% s, % s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (name, email, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth, ))
                connection.commit()
                flash('You have successfully registered !')
                return redirect(url_for('account.login'))
        elif type == 'agent':
            email = request.form['email']
            password = request.form['password']
            cursor.execute('SELECT * FROM agent WHERE agent_email = % s', (email, ))
            account = cursor.fetchone()
            if account:
                flash('Account already exists !')
            else:
                cursor.execute(
                    'INSERT INTO agent(agent_email, password) VALUES (% s, % s)',
                    (email, password, ))
                connection.commit()
                flash('You have successfully registered !')
                return redirect(url_for('account.login'))
        elif type == 'staff':
            username = request.form['username']
            airline_name = request.form['airline_name']
            email = request.form['email']
            password = request.form['password']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            date_of_birth = request.form["date_of_birth"]
            cursor.execute('SELECT * FROM airline_staff WHERE username = % s', (username, ))
            account = cursor.fetchone()
            if account:
                flash('Account already exists !')
            else:
                cursor.execute(
                    'INSERT INTO airline_staff VALUES (% s, % s, %s, %s, %s, %s)',
                    (airline_name, username, password, first_name, last_name, date_of_birth,))
                connection.commit()
                flash('You have successfully registered !')
                return redirect(url_for('account.login'))

    return render_template('register.html')



