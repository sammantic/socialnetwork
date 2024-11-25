from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.db.models.individual import Individual
from app.services.individuals import service_get_all_individuals

client = TestClient(app)


def test_service_get_all_individuals(mocker):
    # Arrange: Create a mock database session
    mock_db = MagicMock(spec=Session)

    # Create mock individuals to return from the mock db
    mock_individuals = [
        Individual(name="Adam Smith"),
        Individual(name="John Obama")
    ]

    # Mock the query method and the .all() call on it to return the mock individuals
    mock_query = mock_db.query.return_value  # Mock the return value of the query() method
    mock_query.all.return_value = mock_individuals

    # Act: Call the service function with the mocked db session
    result = service_get_all_individuals(mock_db)

    # Assert: Verify that the returned data matches the mock individuals
    assert result == mock_individuals

    # Verify that the query method was called once with the Individual model
    mock_db.query.assert_called_once_with(Individual)

    # Verify that the all() method was called once on the query object
    mock_query.all.assert_called_once()

def test_get_all_individual():
    """
    send get request to get all individuals
    :return:
    """
    response = client.get("http://127.0.0.1:8000/v1/individual/")
    assert response.status_code == 200  # Assert status code is 200 (OK)
    assert response.json() == [
        {
            "name": "Ali",
            "individual_id": 1,
            "date_of_birth": "2024-11-23T00:00:00",
            "other_details": "string"
        },
        {
            "name": "hassan",
            "individual_id": 2,
            "date_of_birth": "2024-11-23T00:00:00",
            "other_details": "string"
        },
        {
            "name": "John",
            "individual_id": 6,
            "date_of_birth": "2024-11-23T00:00:00",
            "other_details": None
        },
        {
            "name": "travolta",
            "individual_id": 7,
            "date_of_birth": "2024-11-23T00:00:00",
            "other_details": None
        }
    ]  # Assert response data matches expected output
