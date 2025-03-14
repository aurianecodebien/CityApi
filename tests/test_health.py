import pytest
from unittest.mock import patch, MagicMock
from app import create_app


@pytest.fixture
def client():
    """Crée un client Flask sans base de données réelle."""
    app = create_app(testing=True)
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            yield client


@patch("app.extensions.db.session")
def test_health_check_success(mock_db_session, client):
    """Teste l'endpoint de healthcheck quand la base répond correctement."""
    
    mock_db_session.execute.return_value = None
    response = client.get("/_health")
    assert response.status_code == 204
    mock_db_session.execute.assert_called_once()


@patch("app.extensions.db.session")
def test_health_check_failure(mock_db_session, client):
    """Teste l'endpoint de healthcheck quand la base est en échec."""
    
    mock_db_session.execute.side_effect = Exception("Database connection failed")
    response = client.get("/_health")
    assert response.status_code == 500
    assert response.json == {"status": "unhealthy", "error": "Database connection failed"}
    mock_db_session.execute.assert_called_once()
