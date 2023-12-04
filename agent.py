from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('agent',__name__,url_prefix='/agent')

@bp.route('/my_flights',methods=['GET'])
def my_flights():
    '''
    similar to public.query_flight
    request params:
        airline_name
        flight_num
        DATE(departure_time)
        DATE(arrival_time)
    template data:
        result - rows (dictionary) from the flight table, by default None
        airlines - list of airlines
        login
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))

    prompt = request.args.to_dict()
    req = f"SELECT F.airline_name, F.flight_num, F.departure_airport, F.arrival_airport, F.departure_time, F.arrival_time, F.price\
        FROM flight as F, ticket as T\
        WHERE F.airline_name = T.airline_name AND F.flight_num = T.flight_num AND T.booking_agent_id = {session['username'][6:]}" #AND F.status = 'Upcoming'"
    req += ''.join((f'AND F.{i} = {repr(j)}' for i,j in prompt.items() if j!='' and 'DATE' not in i))
    for time in ["departure_time", "arrival_time"]:
        if f'DATE({time})' in prompt and prompt[f'DATE({time})'] != '':
            req += f'AND F.{time} LIKE "{prompt[f"DATE({time})"]}%"'

    with sql.SQLConnection.Instance().conn.cursor() as cursor:
        cursor.execute('SELECT * FROM airline')
        airlines = [x['name'] for x in cursor.fetchall()]
        cursor.execute(req)
        result = cursor.fetchall()
        #print(result)
    return render_template('my_flights.html', 
        result=result,
        airlines=airlines,
        login={
           'username':session['username'],
           'type': session['type'],
           'profile':'https://www.gstatic.com/android/keyboard/emojikitchen/20220406/u1f349/u1f349_u1f605.png?fbx'})

@bp.route('/commission',methods=['GET'])
def commission():
    '''
    request params:
        start, end - the range of dates aggregated(by default 30days earlier-now)
    template data:
        commission - total amount of commission received
        comm_per_ticket - average commission per ticket booked
        tickets - total number of tickets sold
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))
    
    return render_template('commission.html',
        login={
           'username':session['username'],
           'type': session['type'],
           'profile':'https://www.gstatic.com/android/keyboard/emojikitchen/20220406/u1f349/u1f349_u1f605.png?fbx'})

@bp.route('/customers')
def customers():
    '''
    template data:
        namest - names of top 5 customers based on number of tickets bought in the past 6 months
        tickets - the number of tickets respectively
        namesc - top 5 customers based on amount of commission in the last year.
        commission - the amount of commission respectively
        login
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))
    
    req = 'SELECT C.name, COUNT(T.ticket_id) as CNT FROM customer as C, ticket as T WHERE C.email = T.customer_email GROUP BY C.email ORDER BY COUNT(T.ticket_id) DESC LIMIT 5'
    with sql.SQLConnection.Instance().conn.cursor() as cursor:
        cursor.execute(req)
        result = cursor.fetchall()
        namest = [each['name'] for each in result]
        tickets = [each['CNT'] for each in result]
    return render_template('top_customers.html',
                            namest = namest,
                            tickets = tickets,
                            commission = [5,4,3,2,1],
                            namesc = ['Alice','Bob','Carol','David','Eve'],
                            login={
                                'username':session['username'],
                                'type': session['type'],
                                'profile':'https://www.gstatic.com/android/keyboard/emojikitchen/20220406/u1f349/u1f349_u1f605.png?fbx'}) 