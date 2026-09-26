from flask import Blueprint, jsonify, request

from app.services.booking_service import (
    BOOKINGS,
    create_booking
)


booking_bp = Blueprint(
    "bookings",
    __name__,
    url_prefix="/api/v1"
)


@booking_bp.route("/bookings", methods=["POST"])
def create_booking_api():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    try:
        booking = create_booking(data)

        return jsonify({
            "status": "success",
            "data_type": "demo",
            "message": "Demonstration booking created successfully",
            "booking": booking.to_dict()
        }), 201

    except ValueError as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400


@booking_bp.route("/bookings/<booking_id>", methods=["GET"])
def get_booking(booking_id):

    booking = BOOKINGS.get(booking_id)

    if booking is None:
        return jsonify({
            "status": "error",
            "message": "Booking not found"
        }), 404

    return jsonify({
        "status": "success",
        "data_type": "demo",
        "booking": booking.to_dict()
    }), 200