from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('staff',__name__,url_prefix='/staff')


@bp.route('/my_flights',methods=['GET'])
def my_flights():
    return ""

@bp.route('/manage',methods=['GET','POST'])
def manage():
    return ""

@bp.route('/stats',methods=['GET'])
def stats():
    return ""

@bp.route('/accounts',methods=['GET'])
def accounts():
    return ""

