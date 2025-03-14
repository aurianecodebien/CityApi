import pytest
import json
from unittest.mock import patch, MagicMock
from app import create_app
from app.models.city import City

@pytest.fixture
def client():
    """Crée un client Flask avec un contexte d'application propre."""
    app = create_app(testing=True)
    app.config["TESTING"] = True

    with app.app_context():
        with app.test_client() as client:
            yield client  


@patch("app.extensions.db.session")
def test_add_city(mock_db_session, client):
    """Teste l'insertion d'une ville sans toucher la base."""
    
    city_data = {
        "department_code": "75",
        "insee_code": "75056",
        "zip_code": "75001",
        "name": "Paris",
        "lat": 48.8566,
        "lon": 2.3522
    }

    response = client.post("/city", data=json.dumps(city_data), content_type="application/json")

    mock_db_session.add.assert_called_once()
    assert isinstance(mock_db_session.add.call_args[0][0], City)

    mock_db_session.commit.assert_called_once()

    assert response.status_code == 201
    assert response.json["message"] == "City added successfully"

@patch("app.models.city.City.query")
def test_get_cities(mock_query, client):
    """Teste la récupération de la liste des villes en mockant la base."""
    
    with client.application.app_context():
        mock_city = MagicMock(spec=City)
        mock_city.id = 1
        mock_city.department_code = "75"
        mock_city.insee_code = "75056"
        mock_city.zip_code = "75001"
        mock_city.name = "Paris"
        mock_city.lat = 48.8566
        mock_city.lon = 2.3522

        mock_query.all.return_value = [mock_city]

        response = client.get("/city")

        assert response.status_code == 200

        expected_data = [
            {
                "id": 1,
                "department_code": "75",
                "insee_code": "75056",
                "zip_code": "75001",
                "name": "Paris",
                "lat": 48.8566,
                "lon": 2.3522
            }
        ]
        assert response.json == expected_data

        mock_query.all.assert_called_once()

