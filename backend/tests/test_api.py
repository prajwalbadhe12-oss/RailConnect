import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()

    app.config.update({
        "TESTING": True,
    })

    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"


def test_server_info(client):
    response = client.get("/api/server-info")

    assert response.status_code == 200

    data = response.get_json()

    assert data["application"] == "RailConnect"
    assert data["status"] == "healthy"


def test_get_trains(client):
    response = client.get("/api/v1/trains")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"
    assert data["data_type"] == "demo"
    assert data["count"] > 0
    assert len(data["trains"]) > 0


def test_get_existing_train(client):
    response = client.get("/api/v1/trains/RC101")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"
    assert data["train"]["id"] == "RC101"


def test_get_non_existing_train(client):
    response = client.get("/api/v1/trains/INVALID")

    assert response.status_code == 404

    data = response.get_json()

    assert data["status"] == "error"
    assert data["message"] == "Train not found"


def test_search_trains(client):
    response = client.get(
        "/api/v1/search"
        "?source=Mumbai%20Central"
        "&destination=New%20Delhi"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"
    assert data["count"] > 0
    assert len(data["trains"]) > 0


def test_search_missing_source(client):
    response = client.get(
        "/api/v1/search?destination=New%20Delhi"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["status"] == "error"


def test_search_missing_destination(client):
    response = client.get(
        "/api/v1/search?source=Mumbai%20Central"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["status"] == "error"


def test_create_booking(client):
    payload = {
        "train_id": "RC101",
        "journey_date": "2026-10-15",
        "travel_class": "2A",
        "passengers": [
            {
                "name": "Rahul Sharma",
                "age": 32,
                "gender": "Male",
                "seat_preference": "Window"
            }
        ]
    }

    response = client.post(
        "/api/v1/bookings",
        json=payload
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["status"] == "success"
    assert data["data_type"] == "demo"

    booking = data["booking"]

    assert booking["train_id"] == "RC101"
    assert booking["journey_date"] == "2026-10-15"
    assert booking["travel_class"] == "2A"
    assert booking["status"] == "CONFIRMED"
    assert booking["booking_id"]
    assert booking["pnr"]


def test_create_booking_without_body(client):
    response = client.post(
        "/api/v1/bookings",
        json=None
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["status"] == "error"
    assert data["message"] == "Request body is required"


def test_create_booking_with_invalid_train(client):
    payload = {
        "train_id": "INVALID",
        "journey_date": "2026-10-15",
        "travel_class": "2A",
        "passengers": [
            {
                "name": "Rahul Sharma",
                "age": 32,
                "gender": "Male",
                "seat_preference": "Window"
            }
        ]
    }

    response = client.post(
        "/api/v1/bookings",
        json=payload
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["status"] == "error"
    assert data["message"] == "Train not found"


def test_create_booking_without_passengers(client):
    payload = {
        "train_id": "RC101",
        "journey_date": "2026-10-15",
        "travel_class": "2A",
        "passengers": []
    }

    response = client.post(
        "/api/v1/bookings",
        json=payload
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["status"] == "error"
    assert data["message"] == "At least one passenger is required"
def test_unknown_route_returns_json_error(client):
    response = client.get("/api/v1/unknown")

    assert response.status_code == 404

    data = response.get_json()

    assert data["status"] == "error"
    assert data["message"] == "Resource not found"


def test_method_not_allowed_returns_json_error(client):
    response = client.get("/api/v1/bookings")

    assert response.status_code == 405

    data = response.get_json()

    assert data["status"] == "error"
    assert data["message"] == "Method not allowed"

    'invalid travel class'

def test_create_booking_with_invalid_travel_class(client):
    payload = {
        "train_id": "RC101",
        "journey_date": "2026-10-15",
        "travel_class": "SL",
        "passengers": [
            {
                "name": "Rahul Sharma",
                "age": 32,
                "gender": "Male",
                "seat_preference": "Window"
            }
        ]
    }

    response = client.post(
        "/api/v1/bookings",
        json=payload
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["status"] == "error"
    assert "not available" in data["message"]

    'Invalid age'

def test_create_booking_with_invalid_age(client):
    payload = {
        "train_id": "RC101",
        "journey_date": "2026-10-15",
        "travel_class": "2A",
        "passengers": [
            {
                "name": "Rahul Sharma",
                "age": 150,
                "gender": "Male",
                "seat_preference": "Window"
            }
        ]
    }

    response = client.post(
        "/api/v1/bookings",
        json=payload
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["status"] == "error"
    assert data["message"] == (
        "Passenger age must be between 1 and 120"
    ) 

    'Invalid gender'
def test_create_booking_with_invalid_gender(client):
    payload = {
        "train_id": "RC101",
        "journey_date": "2026-10-15",
        "travel_class": "2A",
        "passengers": [
            {
                "name": "Rahul Sharma",
                "age": 32,
                "gender": "Unknown",
                "seat_preference": "Window"
            }
        ]
    }

    response = client.post(
        "/api/v1/bookings",
        json=payload
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["status"] == "error"
    assert data["message"] == (
        "Passenger gender must be Male, Female, or Other"
    )

    'Test past journey '

def test_create_booking_with_past_journey_date(client):
    payload = {
        "train_id": "RC101",
        "journey_date": "2020-01-01",
        "travel_class": "2A",
        "passengers": [
            {
                "name": "Rahul Sharma",
                "age": 32,
                "gender": "Male",
                "seat_preference": "Window"
            }
        ]
    }

    response = client.post(
        "/api/v1/bookings",
        json=payload
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["status"] == "error"
    assert data["message"] == (
        "Journey date cannot be in the past"
    )
    
def test_create_booking_with_too_many_passengers(client):
    passengers = []

    for number in range(7):
        passengers.append({
            "name": f"Passenger {number + 1}",
            "age": 30,
            "gender": "Male",
            "seat_preference": "No Preference"
        })

    payload = {
        "train_id": "RC101",
        "journey_date": "2026-10-15",
        "travel_class": "2A",
        "passengers": passengers
    }

    response = client.post(
        "/api/v1/bookings",
        json=payload
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["status"] == "error"
    assert data["message"] == (
        "Maximum 6 passengers are allowed per booking"
    )