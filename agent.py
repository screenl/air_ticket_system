from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('agent',__name__,url_prefix='/agent')

@bp.route('/my_flights')
def my_flights():
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
    return render_template('commission.html')

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
    return render_template('top_customers.html',
                           namest = ['Alice','Bob','Carol','David','Eve'],
                           tickets = [5,4,3,2,0],
                           commission = [5,4,3,2,1],
                           namesc = ['Alice','Bob','Carol','David','Eve']) 