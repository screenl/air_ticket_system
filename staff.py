from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
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
    return render_template("stats.html")

@bp.route('/accounts',methods=['GET'])
def accounts():
    return render_template("manage_accounts.html")

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