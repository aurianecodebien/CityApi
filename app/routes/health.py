from sqlalchemy import text
from app.extensions import db
from flask import jsonify, Blueprint

health_bp = Blueprint('health', __name__)


@health_bp.route('/_health', methods=['GET'])
def health_check():
    try:
        db.session.execute(text('SELECT 1'))
        return "", 204
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500