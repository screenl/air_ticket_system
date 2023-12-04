from datetime import date
from dateutil.relativedelta import relativedelta
from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('customer',__name__,url_prefix='/customer')

@bp.route('/my_flights')
def my_flight():
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
    req = f"SELECT F.airline_name, F.flight_num, F.departure_airport, F.arrival_airport, F.departure_time, F.arrival_time, F.price\
        FROM flight as F, ticket as T, customer as C\
        WHERE F.airline_name = T.airline_name AND F.flight_num = T.flight_num AND T.customer_email = C.email AND C.email = '{session['email']}'"
    prompt = request.args.to_dict()
    req += ''.join((f'AND F.{i} = {repr(j)}' for i,j in prompt.items() if j!='' and 'DATE' not in i))
    for time in ["departure_time", "arrival_time"]:
        if f'DATE({time})' in prompt and prompt[f'DATE({time})'] != '':
            req += f'AND {time} LIKE "{prompt[f"DATE({time})"]}%"'
    print(req)
    with sql.SQLConnection.Instance().conn.cursor() as cursor:
        cursor.execute('SELECT * FROM airline')
        airlines = cursor.fetchone().values()
        cursor.execute(req)
        result = cursor.fetchall()
    return render_template('my_flights.html',
        result = result,
        airlines = airlines,
        login={
           'username':session['username'],
           'type': session['type'],
           'profile':'https://www.gstatic.com/android/keyboard/emojikitchen/20220406/u1f349/u1f349_u1f605.png?fbx'})

@bp.route('/spending',methods=['GET'])
def spending():
    '''
    a query page showing the statistics for a customer's spending
    method: get
    request params: 
        start - 6 months earlier by default, 
        end - the current month by default
    template data:
        money - monthly spending
        months - a list of selected months
        login
    '''
    if dict(session) == {}:
        return redirect(url_for('account.login'))
    connection = sql.SQLConnection.Instance().conn
    cursor = connection.cursor()
    start = request.args.get('start') or str(date.today()- relativedelta(months=6))
    end = request.args.get('end') or str(date.today())
    cursor.execute(f'''SELECT DATE_FORMAT(purchased_date,'%Y-%m') as month, sum(price) as spending
                    FROM ticket JOIN flight USING(airline_name,flight_num)
                    WHERE DATE_FORMAT(purchased_date,'%Y-%m') >= DATE_FORMAT('{start}','%Y-%m')
                    AND DATE_FORMAT(purchased_date,'%Y-%m') <= DATE_FORMAT('{end}','%Y-%m')
                    AND customer_email = '{session['email']}'
                    GROUP BY DATE_FORMAT(purchased_date,'%Y-%m')
                ''', 
                )
    print(f'''SELECT DATE_FORMAT(purchased_date,'%Y-%m') as month, sum(price) as spending
                    FROM ticket JOIN flight USING(airline_name,flight_num)
                    WHERE DATE_FORMAT(purchased_date,'%Y-%m') >= DATE_FORMAT('{start}','%Y-%m')
                    AND DATE_FORMAT(purchased_date,'%Y-%m') <= DATE_FORMAT('{end}','%Y-%m')
                    AND customer_email = '{session['email']}'
                    GROUP BY DATE_FORMAT(purchased_date,'%Y-%m')
                ''')
    p = {k['month']:k['spending'] for k in cursor.fetchall()}
    money = []
    months = []
    s = date.fromisoformat(start)
    e = date.fromisoformat(end)
    s.replace(day=1)
    e.replace(day=1)
    while s<e:
        s+=relativedelta(months=1)
        months.append(s.strftime("%Y-%m"))
        money.append(p.get(s.strftime("%Y-%m"),0))
    return render_template('spending.html',
                            money=money,
                            months=months,
                            login={
                                'username':session['username'],
                                'type': session['type'],
                                'profile':'https://www.gstatic.com/android/keyboard/emojikitchen/20220406/u1f349/u1f349_u1f605.png?fbx'}) 