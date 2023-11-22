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
        result - a single row (dictionary) from the flight table, by default None
        airlines - list of airlines
        login
    '''
    return render_template('my_flights.html')

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
    return render_template('spending.html',
                           money=[550, 490, 20 , 240, 400, 300],
                           months=["2023-06", "2023-07", "2023-08", "2023-09", "2023-10","2023-11"]) 
