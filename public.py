
from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('public',__name__,url_prefix='/public')

@bp.route('/search_flight',methods=['GET'])
def query_flight():
    #todo: session
    prompt = request.args.to_dict()
    prompt['status']='Upcoming'
    req = 'SELECT * FROM flight WHERE ' + ' AND '.join((f'{i} = {repr(j)}' for i,j in prompt.items() if j!=''))
    print(req)
    
    with sql.SQLConnection.Instance().conn.cursor() as cursor:
        cursor.execute('SELECT * FROM airline')
        airlines = map(lambda x: [*x.values()][0],cursor.fetchall())
        cursor.execute('SELECT name FROM airport')
        airports = map(lambda x: [*x.values()][0],cursor.fetchall())
        cursor.execute(req)
        return render_template('search_for_flight.html',result=list(cursor.fetchall()),airlines=list(airlines),airports=list(airports))
    
@bp.route('/home')
def home():
    '''
    template params:
    
    uses session
    '''
    #return render_template("about.html")
    return render_template("about.html",
       login={
           'username':'John Doe',
           'type': 'staff',
           'profile':'https://www.gstatic.com/android/keyboard/emojikitchen/20220406/u1f349/u1f349_u1f605.png?fbx'}
    ) 

@bp.route('/status',methods=['GET'])
def flight_status():
    '''
    request params:
    result - a single row (dictionary) from the flight table, elsewise None
    airlines - list of airlines

    uses session
    '''
    return render_template('flight_status.html')
    #return render_template("flight_status.html",result={'airline_name':'CE','flight_num':555,'arrival_airport':'PVG','departure_airport':'JFK','status':'Delayed'})
    