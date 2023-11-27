from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

bp = Blueprint('staff',__name__,url_prefix='/staff')


@bp.route('/my_flights',methods=['GET'])
def my_flights():
    return render_template("my_flights_staff.html")

@bp.route('/manage',methods=['GET','POST'])
def manage():
    return render_template("manage_info.html")

@bp.route('/stats',methods=['GET'])
def stats():
    return render_template("stats.html",
                           top_agent_sales = ['a','b','c','d','e'],
                           top_agent_commissions = ['a','b','c','d','e'],
                           top_dest_month = ['a','b','c'],
                           top_dest_year = ['a','b','c'],
                           most_frequent = 'Otto',
                           revenue_customer = 5,
                           revenue_agent = 6)

@bp.route('/accounts',methods=['GET'])
def accounts():
    return render_template("manage_accounts.html")

'''
------------------------------------------
Database shit
------------------------------------------
'''
@bp.route('/get_monthly_sales',methods=['GET'])
def get_monthly_sales():
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
    return jsonify({'flights':[{'number':5,'from':'i','to':'t'},{'number':5,'from':'i','to':'t'}]})


'''
------------------------------------------
More Database shit
------------------------------------------
'''

@bp.route('/grant_permission',methods=['POST'])
def grant_permission():
    return ''

@bp.route('/add_agent',methods=['POST'])
def add_agent():
    return ''

@bp.route('/add_flight',methods=['POST'])
def add_flight():
    return ''

@bp.route('/add_airport',methods=['POST'])
def add_airport():
    return ''

@bp.route('/add_airplane',methods=['POST'])
def add_airplane():
    return ''