from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
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
    
    print(request.args)
    params = request.args.to_dict()
    print(params.values())
    if '' not in params.values():
        airline_name = params['airline_name']
        flight_num = params['flight_num']
        departure_time = params['DATE(departure_time)']
        arrival_time = params['DATE(arrival_time)']
        with sql.SQLConnection.Instance().conn.cursor() as cursor:
            #print("SELECT * FROM flight WHERE airline_name = %s AND flight_num = % s AND departure_time LIKE '% s%%' AND arrival_time LIKE '% s%%'", (airline_name, flight_num, departure_time, arrival_time,))
            #cursor.execute("SELECT * FROM flight WHERE airline_name = % s AND flight_num = % s AND departure_time LIKE % s%% AND arrival_time LIKE % s%%;", (airline_name, flight_num, departure_time, arrival_time,))
            print(f"SELECT * FROM flight WHERE airline_name = {airline_name} AND flight_num = {flight_num} AND departure_time LIKE '{departure_time}%' AND arrival_time LIKE '{arrival_time}%';")
            cursor.execute(f"SELECT * FROM flight WHERE airline_name = '{airline_name}' AND flight_num = {flight_num} AND departure_time LIKE '{departure_time}%' AND arrival_time LIKE '{arrival_time}%';")
            result = cursor.fetchone()
            print(result)
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
    return jsonify({'message':'success'})

@bp.route('redirect',methods=['GET'])
def redir():
    return render_template('redirecting.html',message=request.args.get('message',''),url=request.args.get('url','/'))