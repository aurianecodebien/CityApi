import os
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

def create_app(testing=False):
    from .extensions import db
    from .routes.city import city_bp
    from .routes.health import health_bp

    app = Flask(__name__)
    metrics = PrometheusMetrics(app)

    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        CITY_API_DB_URL = os.getenv('CITY_API_DB_URL')
        CITY_API_DB_USER = os.getenv('CITY_API_DB_USER')
        CITY_API_DB_PWD = os.getenv('CITY_API_DB_PWD')

        if not all([CITY_API_DB_URL, CITY_API_DB_USER, CITY_API_DB_PWD]):
            raise ValueError("CITY_API_DB_URL, CITY_API_DB_USER et CITY_API_DB_PWD must be defined")

        app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{CITY_API_DB_USER}:{CITY_API_DB_PWD}@{CITY_API_DB_URL}'

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = testing

    db.init_app(app)

    app.register_blueprint(city_bp)
    app.register_blueprint(health_bp)

    return app
