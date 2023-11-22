from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('customer',__name__,url_prefix='/customer')

@bp.route('/my_flights')
def my_flight():
    return ''

@bp.route('/spending',methods=['GET'])
def spending():
    '''
    a query page showing the statistics for a customer's spending
    method: get
    request params: time_start(6 months earlier by default), time_end(the current month by default)

    '''
    return ''
