from . import sql 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('agent',__name__,url_prefix='/agent')

@bp.route('/commission',methods=['GET'])
def commission():
    return "comm"

@bp.route('/customers',methods=['GET'])
def customers():
    return "customers"