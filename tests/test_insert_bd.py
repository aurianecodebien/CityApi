import pytest
from unittest.mock import patch, MagicMock
from app import create_app
from app.extensions import db
from app.models.city import City

@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_db_session():
    with patch("app.extensions.db.session") as mock_session:
        yield mock_session

def test_add_city(client, mock_db_session):
    """Test l'insertion d'une ville dans la base de données."""
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()

    city_data = {
        "id": 1,
        "department_code": "75",
        "insee_code": "75056",
        "zip_code": "75000",
        "name": "Paris",
        "lat": 48.8566,
        "lon": 2.3522
    }

    response = client.post("/city", json=city_data)

    assert response.status_code == 201
    assert response.get_json() == {"message": "City added successfully"}

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()

def test_get_cities(client, mock_db_session):
    """Test la récupération de la liste des villes."""
    mock_city = City(
        id=1,
        department_code="75",
        insee_code="75056",
        zip_code="75000",
        name="Paris",
        lat=48.8566,
        lon=2.3522
    )

    with patch("app.models.city.City.query") as mock_query:
        mock_query.all.return_value = [mock_city]

        response = client.get("/city")


        assert response.status_code == 200
        assert response.get_json() == [{
            "id": 1,
            "department_code": "75",
            "insee_code": "75056",
            "zip_code": "75000",
            "name": "Paris",
            "lat": 48.8566,
            "lon": 2.3522
        }]
