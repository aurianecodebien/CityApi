from ..extensions import db
from ..models.city import City
from flask import request, jsonify
from flask import Blueprint

city_bp = Blueprint('city', __name__)

@city_bp.route('/city', methods=['GET'])
def get_cities():
    cities = City.query.all()
    city_list = [{
        "id": city.id,
        "department_code": city.department_code,
        "insee_code": city.insee_code,
        "zip_code": city.zip_code,
        "name": city.name,
        "lat": city.lat,
        "lon": city.lon
    } for city in cities]
    return jsonify(city_list), 200

@city_bp.route('/city', methods=['POST'])
def add_city():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    try:
        new_city = City(
            id=data['id'],
            department_code=data['department_code'],
            insee_code=data.get('insee_code'),
            zip_code=data.get('zip_code'),
            name=data['name'],
            lat=data['lat'],
            lon=data['lon']
        )
        db.session.add(new_city)
        db.session.commit()
        return jsonify({"message": "City added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@city_bp.route('/cities', methods=['POST'])
def add_cities():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    msg = []
    try:
        for city in data:
            new_city = City(
                id=city['id'],
                department_code=city['department_code'],
                insee_code=city.get('insee_code'),
                zip_code=city.get('zip_code'),
                name=city['name'],
                lat=city['lat'],
                lon=city['lon']
            )
            db.session.add(new_city)
            msg.append(f"{city['name']} added successfully")
        
        db.session.commit()
        return jsonify({"message": msg}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
