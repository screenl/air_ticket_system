from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

bp = Blueprint('staff',__name__,url_prefix='/staff')


@bp.route('/my_flights',methods=['GET'])
def my_flights():
    '''
    template data:
    result - list of flights
    login
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))
    connection = sql.SQLConnection.Instance().conn
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT F.* FROM flight as F, airline_staff as S WHERE F.airline_name = S.airline_name and S.username = %s', (session['username']))
    result = cursor.fetchall()
    return render_template("my_flights_staff.html",
        result = result,
        login={'username':session['username'],
                'type': session['type'],
                'profile':'https://www.gstatic.com/android/keyboard/emojikitchen/20220406/u1f349/u1f349_u1f605.png?fbx'})

@bp.route('/manage',methods=['GET','POST'])
def manage():
    '''
    template data:
    airports - list of airports
    login
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))

    connection = sql.SQLConnection.Instance().conn
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM airport')
    airports = [each['name'] for each in cursor.fetchall()]    
    return render_template("manage_info.html",
        airports = airports,
        login={'username':session['username'],
                'type': session['type'],
                'profile':'https://www.gstatic.com/android/keyboard/emojikitchen/20220406/u1f349/u1f349_u1f605.png?fbx'})

@bp.route('/stats',methods=['GET'])
def stats():
    '''
    template data:
    top_agent_sales - Top 5 booking agents based on number of tickets sales for the past month 
    top_agent_commissions - Top 5 booking agents based on the amount of commission received for the last year
    top_dest_month - top 3 popular destinations last 3 months
    top_dest_year - top 3 popular destinations last year
    most_frequent - most frequent customer name
    revenue_customer - the revenue via customers last month
    revenue_agent - the revenue via agents last month
    revenue_customer_y - the revenue via customers last year
    revenue_agent_y - the revenue via agents last year
    login
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))

    return render_template("stats.html",
                           top_agent_sales = ['a','b','c','d','e'],
                           top_agent_commissions = ['a','b','c','d','e'],
                           top_dest_month = ['a','b','c'],
                           top_dest_year = ['a','b','c'],
                           most_frequent = 'Otto',
                           revenue_customer = 5,
                           revenue_agent = 6,
                           revenue_customer_y = 5,
                           revenue_agent_y = 6,
                           login={'username':session['username'],
                                'type': session['type'],
                                'profile':'https://www.gstatic.com/android/keyboard/emojikitchen/20220406/u1f349/u1f349_u1f605.png?fbx'})

@bp.route('/accounts',methods=['GET'])
def accounts():
    '''
    template data:
    login
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))

    return render_template("manage_accounts.html",
        login={'username':session['username'],
                'type': session['type'],
                'profile':'https://www.gstatic.com/android/keyboard/emojikitchen/20220406/u1f349/u1f349_u1f605.png?fbx'})

'''
------------------------------------------
Database shit
------------------------------------------
'''
@bp.route('/get_monthly_sales',methods=['GET'])
def get_monthly_sales():
    '''
    request params:
    start
    end
    
    return
    jsonified data(example below)
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))

    return jsonify({
        'total_sales':21,
        'monthly_sales':[
            {'month':'2022-3','sales':5},
            {'month':'2022-4','sales':5},
            {'month':'2022-5','sales':6},
            {'month':'2022-6','sales':5},
        ]
    })

@bp.route('/get_customer_flights',methods=['GET'])
def get_customer_flights():
    '''
    request params:
    email - the email of the customer
    
    return
    jsonified data(example below)
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))

    return jsonify({'flights':[{'number':5,'from':'i','to':'t'},{'number':5,'from':'i','to':'t'}]})


'''
------------------------------------------
More Database shit
------------------------------------------
'''

@bp.route('/change_status',methods=['POST'])
def change_status():
    '''
    request data:
    airline_name
    flight_num
    status
    '''

    if dict(session) == {}:
        return jsonify({'message' : 'Only an Admin or an Operator can change status!'}),201
    connection = sql.SQLConnection.Instance().conn
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM permission WHERE username = %s AND (permission = "Admin" OR permission = "Operator")', (session['username'],))
    if not cursor.fetchone():
        return  jsonify({'message' : 'Only an Admin or an Operator can change status!'}),201
    airline_name = request.form['airline_name']
    flight_num = int(request.form['flight_num'])
    status = request.form['status']
    cursor.execute('UPDATE flight SET status = %s WHERE airline_name = %s AND flight_num = %s', (status,airline_name,flight_num,))
    connection.commit()
    return jsonify({'message':'success!'})

@bp.route('/grant_permission',methods=['POST'])
def grant_permission():
    '''
    request data:
    username - the username of the to-be-granted staff 
    permission

    redirect to message page
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))
    
    username = request.form['username']
    permission = request.form['permission']
    connection = sql.SQLConnection.Instance().conn
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM permission WHERE username = %s AND permission = "Admin"', (session['username'],))
    if not cursor.fetchone():
        return render_template('redirecting.html', message = 'Only an Admin can grant permission!', url = url_for('staff.accounts'))
    
    cursor.execute('SELECT * FROM airline_staff WHERE username = %s', (username,))
    if not cursor.fetchone():
        return render_template('redirecting.html', message = 'Staff does not exist!', url = url_for('staff.accounts'))
    
    cursor.execute('SELECT airline_name FROM airline_staff WHERE username = %s', (session['username'],))
    airline_name = cursor.fetchone()['airline_name']
    cursor.execute('SELECT * FROM airline_staff WHERE username = %s AND airline_name = %s', (username, airline_name))
    if not cursor.fetchone():
        return render_template('redirecting.html', message = 'You can grant permission to staff in the same airline!', url = url_for('staff.accounts'))
    
    cursor.execute('SELECT * FROM permission WHERE username = %s AND permission = %s', (username, permission,))
    if cursor.fetchone():
        return render_template('redirecting.html', message = 'Staff already authorized!', url = url_for('staff.accounts'))

    cursor.execute('INSERT INTO permission VALUES(%s, %s)', (username, permission,))
    connection.commit()
    return render_template('redirecting.html', message = 'Permission successfully granted!', url = url_for('staff.accounts'))

@bp.route('/add_agent',methods=['POST'])
def add_agent():
    '''
    request data:
    email - the email of the agent to be added

    redirect to message page
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))

    email = request.form['email']
    connection = sql.SQLConnection.Instance().conn
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM permission WHERE username = %s AND permission = "Admin"', (session['username'],))
    if not cursor.fetchone():
        return render_template('redirecting.html', message = 'Only an Admin can add an agent!', url = url_for('staff.accounts'))
    cursor.execute('SELECT * FROM agent WHERE agent_email = %s', (email,))
    if not cursor.fetchone():
        return render_template('redirecting.html', message = 'Agent does not exist!', url = url_for('staff.manage'))
    cursor.execute('SELECT airline_name FROM airline_staff WHERE username = %s', (session['username'],))
    airline_name = cursor.fetchone()['airline_name']
    cursor.execute('SELECT * FROM works_for WHERE airline_name = %s AND agent_email = %s', (airline_name, email,))
    if cursor.fetchone():
        return render_template('redirecting.html', message = 'Agent already works for the airline!', url = url_for('staff.accounts'))
    cursor.execute('INSERT INTO works_for VALUES(%s, %s)', (airline_name, email,))
    connection.commit()
    return render_template('redirecting.html', message = 'Successfully added a flight!', url = url_for('staff.accounts'))


@bp.route('/add_flight',methods=['POST'])
def add_flight():
    '''
    request data:
    departure_airport
    arrival_airport
    departure_time
    arrival_time
    plane
    price
    status
    
    redirect to the message page
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))

    flight_num = request.form['flight_num']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    departure_time = request.form['departure_time']
    arrival_time = request.form['arrival_time']
    plane = request.form['plane']
    price = request.form['price']
    status = request.form['status']

    connection = sql.SQLConnection.Instance().conn
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM permission WHERE username = %s AND permission = "Admin"', (session['username'],))
    if not cursor.fetchone():
        return render_template('redirecting.html', message = 'Only an Admin can add a flight!', url = url_for('staff.manage'))
    cursor.execute('SELECT airline_name FROM airline_staff WHERE username = %s', (session['username'],))
    airline_name = cursor.fetchone()['airline_name']
    cursor.execute('SELECT * FROM airplane WHERE airline_name = %s AND id = %s', (airline_name, plane,))
    if not cursor.fetchone():
        return render_template('redirecting.html', message = 'Airplane does not exist!', url = url_for('staff.manage'))
    cursor.execute('INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)', (airline_name, flight_num, departure_airport, arrival_airport, plane, arrival_time, departure_time, price, status,))
    connection.commit()
    return render_template('redirecting.html', message = 'Successfully added a flight !', url = url_for('staff.manage'))

@bp.route('/add_airport',methods=['POST'])
def add_airport():
    '''
    request data:
    name
    city
    
    redirect to the message page
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))

    name = request.form['name']
    city = request.form['city']
    connection = sql.SQLConnection.Instance().conn
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM permission WHERE username = %s AND permission = "Admin"', (session['username'],))
    if not cursor.fetchone():
        return render_template('redirecting.html', message = 'Only an Admin can add an airport!', url = url_for('staff.manage'))
    cursor.execute('SELECT * FROM airport WHERE name = %s AND city = %s', (name, city,))
    if cursor.fetchone():
        return render_template('redirecting.html', message = 'Airport already exists!', url = url_for('staff.manage'))
    cursor.execute('INSERT INTO airport VALUES(%s, %s)', (name, city,))
    connection.commit()
    return render_template('redirecting.html', message = 'Successfully added an airplane!', url = url_for('staff.manage'))

@bp.route('/add_airplane',methods=['POST'])
def add_airplane():
    '''
    request data:
    id
    seats

    when completed, redirect to the message page
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))

    id = request.form['id']
    seats = request.form['seats']
    connection = sql.SQLConnection.Instance().conn
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM permission WHERE username = %s AND permission = "Admin"', (session['username'],))
    if not cursor.fetchone():
        return render_template('redirecting.html', message = 'Only an Admin can add an airplane!', url = url_for('staff.manage'))
    cursor.execute('SELECT * FROM airplane as P, airline_staff as S WHERE P.airline_name = S.airline_name AND P.id = %s AND S.username = %s', (id, session['username'],))
    if cursor.fetchone():
        return render_template('redirecting.html', message = 'Airplane with the given ID already exists!', url = url_for('staff.manage'))
    cursor.execute('SELECT airline_name FROM airline_staff WHERE username = %s', (session['username'],))
    airline_name = cursor.fetchone()['airline_name']
    cursor.execute('INSERT INTO airplane VALUES(%s, %s, %s)', (airline_name, id, seats,))
    connection.commit()
    return render_template('redirecting.html', message = 'Successfully added an airplane!', url = url_for('staff.manage'))

