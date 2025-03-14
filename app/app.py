import os
from flask import Flask



# ENV
CITY_API_ADDR = os.getenv('CITY_API_ADDR', '127.0.0.1')
CITY_API_PORT = int(os.getenv('CITY_API_PORT', 2022))
CITY_API_DB_URL = os.getenv('CITY_API_DB_URL')
CITY_API_DB_USER = os.getenv('CITY_API_DB_USER')
CITY_API_DB_PWD = os.getenv('CITY_API_DB_PWD')
if not all([CITY_API_DB_URL, CITY_API_DB_USER, CITY_API_DB_PWD]):
    raise ValueError("CITY_API_DB_URL, CITY_API_DB_USER et CITY_API_DB_PWD must be defined")



def create_app():
    from .extensions import db
    from .routes.city import city_bp
    from .routes.health import health_bp
    # App config
    app = Flask(__name__)
    
    app.config['SERVER_NAME'] = f'{CITY_API_ADDR}:{CITY_API_PORT}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{CITY_API_DB_USER}:{CITY_API_DB_PWD}@{CITY_API_DB_URL}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # DB
    db.init_app(app)
    
    # Routes
    app.register_blueprint(city_bp)
    app.register_blueprint(health_bp)
    return app

def run(app):
    print("Trying to run")
    app.run(host=CITY_API_ADDR, port=CITY_API_PORT, debug=True)
    print("Finished running")
