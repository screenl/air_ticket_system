from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Response
)

bp = Blueprint('public',__name__,url_prefix='/public')

@bp.route('/search_flight',methods=['GET'])
def query_flight():

    prompt = request.args.to_dict()
    prompt['status']='Upcoming'
    req = 'SELECT * FROM flight WHERE ' + ' AND '.join((f'{i} = {repr(j)}' for i,j in prompt.items() if j!='' and 'DATE' not in i))
    for time in ["departure_time", "arrival_time"]:
        if f'DATE({time})' in prompt and prompt[f'DATE({time})'] != '':
            req += f'AND {time} LIKE "{prompt[f"DATE({time})"]}%"'
    #print(req)

    with sql.SQLConnection.Instance().conn.cursor() as cursor:
        cursor.execute('SELECT * FROM airline')
        airlines = [x['name'] for x in cursor.fetchall()]
        cursor.execute('SELECT name FROM airport')
        airports = [x['name'] for x in cursor.fetchall()]
        cursor.execute(req)
        result = cursor.fetchall()

    login = {'profile':'https://www.gstatic.com/android/keyboard/emojikitchen/20220406/u1f349/u1f349_u1f605.png?fbx'}
    if 'username' in session:
        login['username'] = session['username']
        login['type'] = session['type']
    else:
        login['username'] = 'Visitor'
        login['type'] = 'visitor'
    return render_template('search_for_flight.html',
        result=result,
        airlines=airlines,
        airports=airports,
        login=login)
    
@bp.route('/home')
def home():
    '''
    template data:
        login
    '''

    #return render_template("about.html")
    login = {'profile':'https://www.gstatic.com/android/keyboard/emojikitchen/20220406/u1f349/u1f349_u1f605.png?fbx'}
    if 'username' in session:
        login['username'] = session['username']
        login['type'] = session['type']
    else:
        login['username'] = 'Visitor'
        login['type'] = 'visitor'
    return render_template("about.html",
        login=login) 

@bp.route('/status',methods=['GET'])
def flight_status():
    '''
    request params:
        airline_name
        flight_num
        DATE(departure_time)
        DATE(arrival_time)
    template data:
        result - a single row (dictionary) from the flight table, by default None
        airlines - list of airlines
        login
    '''
    
    #print(request.args)
    params = request.args.to_dict()
    #print(params.values())
    if params != {} and '' not in params.values():
        airline_name = params['airline_name']
        flight_num = params['flight_num']
        departure_time = params['DATE(departure_time)']
        arrival_time = params['DATE(arrival_time)']
        with sql.SQLConnection.Instance().conn.cursor() as cursor:
            #print("SELECT * FROM flight WHERE airline_name = %s AND flight_num = % s AND departure_time LIKE '% s%%' AND arrival_time LIKE '% s%%'", (airline_name, flight_num, departure_time, arrival_time,))
            #cursor.execute("SELECT * FROM flight WHERE airline_name = % s AND flight_num = % s AND departure_time LIKE % s%% AND arrival_time LIKE % s%%;", (airline_name, flight_num, departure_time, arrival_time,))
            #print(f"SELECT * FROM flight WHERE airline_name = {airline_name} AND flight_num = {flight_num} AND departure_time LIKE '{departure_time}%' AND arrival_time LIKE '{arrival_time}%';")
            cursor.execute(f"SELECT * FROM flight WHERE airline_name = '{airline_name}' AND flight_num = {flight_num} AND departure_time LIKE '{departure_time}%' AND arrival_time LIKE '{arrival_time}%';")
            result = cursor.fetchone()
            #print(result)
    else:
        result = None
    with sql.SQLConnection.Instance().conn.cursor() as cursor:
        cursor.execute('SELECT * FROM airline')
        airlines = map(lambda x: [*x.values()][0],cursor.fetchall())
    login = {'profile':'https://www.gstatic.com/android/keyboard/emojikitchen/20220406/u1f349/u1f349_u1f605.png?fbx'}
    if 'username' in session:
        login['username'] = session['username']
        login['type'] = session['type']
    else:
        login['username'] = 'Visitor'
        login['type'] = 'visitor'
    return render_template('flight_status.html', 
            result = result,
            airlines = airlines,
            login=login) 
    #return render_template("flight_status.html",result={'airline_name':'CE','flight_num':555,'arrival_airport':'PVG','departure_airport':'JFK','status':'Delayed'})

@bp.route('/purchase_flight',methods=['POST'])
def purchase_flight():
    connection = sql.SQLConnection.Instance().conn
    cursor = connection.cursor()
    airline_name = request.form["airline_name"]
    flight_num = request.form["flight_num"]
    if session['type'] == 'agent':
        buy_for = request.form['buy_for']
        #print(buy_for)
        cursor.execute('SELECT * FROM customer WHERE email = %s', (buy_for, ))
        result = cursor.fetchone()
        #print(result)
        if not result:
            return jsonify({'message':'plane is full'}),201
        id = session['username'][6:]
    elif session['type'] == 'customer':
        buy_for = session['email']
        id = 'NULL'
    #if session['type'] == 'customer':
    cursor.execute('''SELECT COUNT(ticket_id) as c
                   FROM ticket JOIN flight USING(airline_name,flight_num)
                   WHERE airline_name = %s 
                   AND flight_num = %s''', (airline_name, flight_num,))
    cnt = cursor.fetchone()['c']
    cursor.execute('''SELECT *
                   FROM flight JOIN airplane ON flight.plane=airplane.id AND flight.airline_name=airplane.airline_name
                   WHERE flight.airline_name = %s 
                   AND flight.flight_num = %s''', (airline_name, flight_num,))
    try:
        seats = cursor.fetchone()['seats']
    except:
        seats = 999
    if cnt < seats:
        cursor.execute(
        'INSERT INTO ticket (airline_name, customer_email, flight_num, booking_agent_id, ticket_id, purchased_date) VALUES (% s, %s, %s, %s, NULL, CURRENT_DATE())', (airline_name, buy_for, flight_num, id,))
        connection.commit()
        return jsonify({'message':'success'}),200
    else:
        return jsonify({'message':'plane is full'}),202

@bp.route('redirect',methods=['GET'])
def redir():
    return render_template('redirecting.html',message=request.args.get('message',''),url=request.args.get('url','/'))