from app.extensions import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_code = db.Column(db.String(10), nullable=False)
    insee_code = db.Column(db.String(20), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
