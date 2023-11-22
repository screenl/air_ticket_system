import os

from flask import Flask,redirect
from . import sql, staff




def create_app(test_config=None):
    # create and configure the app
    
    sql.SQLConnection.Instance()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.route('/')(lambda : redirect("/public/home", code=302))

    from . import public, account, agent, customer
    app.register_blueprint(public.bp)
    app.register_blueprint(account.bp) 
    app.register_blueprint(staff.bp)
    app.register_blueprint(agent.bp)
    app.register_blueprint(customer.bp)
    return app
