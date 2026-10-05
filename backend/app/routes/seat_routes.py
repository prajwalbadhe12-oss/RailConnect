from flask import Blueprint, jsonify

from app.services.seat_service import get_seats_by_schedule


seat_bp = Blueprint(
    "seats",
    __name__,
    url_prefix="/api/v1"
)


@seat_bp.route("/schedules/<int:schedule_id>/seats", methods=["GET"])
def get_schedule_seats(schedule_id):
    seats = get_seats_by_schedule(schedule_id)

    return jsonify({
        "status": "success",
        "data_type": "database",
        "schedule_id": schedule_id,
        "count": len(seats),
        "seats": seats
    }), 200