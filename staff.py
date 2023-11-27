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
    return render_template("my_flights_staff.html",result = [])

@bp.route('/manage',methods=['GET','POST'])
def manage():
    '''
    template data:
    airports - list of airports
    login
    '''
    return render_template("manage_info.html")

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
    return render_template("stats.html",
                           top_agent_sales = ['a','b','c','d','e'],
                           top_agent_commissions = ['a','b','c','d','e'],
                           top_dest_month = ['a','b','c'],
                           top_dest_year = ['a','b','c'],
                           most_frequent = 'Otto',
                           revenue_customer = 5,
                           revenue_agent = 6,
                           revenue_customer_y = 5,
                           revenue_agent_y = 6)

@bp.route('/accounts',methods=['GET'])
def accounts():
    '''
    template data:
    login
    '''
    return render_template("manage_accounts.html")

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
    return ''

@bp.route('/grant_permission',methods=['POST'])
def grant_permission():
    '''
    request data:
    username - the username of the to-be-granted staff 
    permission

    redirect to message page
    '''
    return ''

@bp.route('/add_agent',methods=['POST'])
def add_agent():
    '''
    request data:
    email - the email of the agent to be added

    redirect to message page
    '''
    return ''

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
    return ''

@bp.route('/add_airport',methods=['POST'])
def add_airport():
    '''
    request data:
    name
    city
    
    redirect to the message page
    '''
    return ''

@bp.route('/add_airplane',methods=['POST'])
def add_airplane():
    '''
    request data:
    id
    seats

    when completed, redirect to the message page
    '''
    return ''

