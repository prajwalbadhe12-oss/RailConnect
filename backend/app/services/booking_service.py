import uuid
import logging
from datetime import date

from app.data import TRAINS
from app.models.booking_model import Booking, Passenger


BOOKINGS = {}

logger = logging.getLogger("RailConnect")

MAX_PASSENGERS = 6

ALLOWED_GENDERS = {
    "Male",
    "Female",
    "Other"
}

ALLOWED_SEAT_PREFERENCES = {
    "Window",
    "Aisle",
    "Lower",
    "Middle",
    "Upper",
    "No Preference"
}


def generate_booking_id():
    return f"BK-{uuid.uuid4().hex[:8].upper()}"


def generate_pnr():
    return uuid.uuid4().hex[:10].upper()


def validate_journey_date(journey_date):
    if not isinstance(journey_date, str) or not journey_date.strip():
        raise ValueError("Journey date is required")

    try:
        parsed_date = date.fromisoformat(journey_date)
    except ValueError:
        raise ValueError(
            "Journey date must be in YYYY-MM-DD format"
        )

    if parsed_date < date.today():
        raise ValueError(
            "Journey date cannot be in the past"
        )


def validate_passenger(passenger):
    if not isinstance(passenger, dict):
        raise ValueError(
            "Each passenger must be a valid object"
        )

    name = passenger.get("name")

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Passenger name is required")

    name = name.strip()

    if len(name) < 2:
        raise ValueError(
            "Passenger name must contain at least 2 characters"
        )

    age = passenger.get("age")

    if age is None:
        raise ValueError("Passenger age is required")

    try:
        age = int(age)
    except (TypeError, ValueError):
        raise ValueError(
            "Passenger age must be a valid number"
        )

    if age < 1 or age > 120:
        raise ValueError(
            "Passenger age must be between 1 and 120"
        )

    gender = passenger.get("gender")

    if gender not in ALLOWED_GENDERS:
        raise ValueError(
            "Passenger gender must be Male, Female, or Other"
        )

    seat_preference = passenger.get(
        "seat_preference",
        "No Preference"
    )

    if seat_preference not in ALLOWED_SEAT_PREFERENCES:
        raise ValueError(
            "Invalid seat preference"
        )

    return Passenger(
        name=name,
        age=age,
        gender=gender,
        seat_preference=seat_preference
    )


def create_booking(booking_request):

    if not isinstance(booking_request, dict):
        raise ValueError(
            "Invalid booking request"
        )

    train_id = booking_request.get("train_id")

    if not isinstance(train_id, str) or not train_id.strip():
        raise ValueError("Train ID is required")

    train_id = train_id.strip()

    train = next(
        (
            train
            for train in TRAINS
            if train["id"] == train_id
        ),
        None
    )

    if train is None:
        raise ValueError("Train not found")

    journey_date = booking_request.get("journey_date")

    validate_journey_date(journey_date)

    travel_class = booking_request.get("travel_class")

    if not isinstance(travel_class, str) or not travel_class.strip():
        raise ValueError("Travel class is required")

    travel_class = travel_class.strip().upper()

    if travel_class not in train["classes"]:
        raise ValueError(
            f"Travel class {travel_class} is not available "
            f"for this train"
        )

    passenger_data = booking_request.get("passengers")

    if not isinstance(passenger_data, list):
        raise ValueError(
            "Passengers must be provided as a list"
        )

    if len(passenger_data) == 0:
        raise ValueError(
            "At least one passenger is required"
        )

    if len(passenger_data) > MAX_PASSENGERS:
        raise ValueError(
            f"Maximum {MAX_PASSENGERS} passengers are allowed "
            f"per booking"
        )

    passengers = []

    for passenger_data_item in passenger_data:
        passenger = validate_passenger(
            passenger_data_item
        )

        passengers.append(passenger)

    total_amount = train["fare"] * len(passengers)

    booking = Booking(
        booking_id=generate_booking_id(),
        pnr=generate_pnr(),
        train_id=train["id"],
        train_name=train["name"],
        source=train["source"],
        destination=train["destination"],
        journey_date=journey_date,
        travel_class=travel_class,
        passengers=passengers,
        total_amount=total_amount
    )

    BOOKINGS[booking.booking_id] = booking

    logger.info(
        "Demo booking created | booking_id=%s | train_id=%s | "
        "passengers=%s | amount=%s",
        booking.booking_id,
        booking.train_id,
        len(booking.passengers),
        booking.total_amount
    )

    return booking