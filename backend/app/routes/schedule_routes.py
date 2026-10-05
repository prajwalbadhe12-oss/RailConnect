from flask import Blueprint, jsonify, request

from app.services.schedule_service import get_schedule_availability


schedule_bp = Blueprint(
    "schedules",
    __name__,
    url_prefix="/api/v1"
)


@schedule_bp.route("/schedules", methods=["GET"])
def get_schedules():
    source = request.args.get("source")
    destination = request.args.get("destination")
    journey_date = request.args.get("journey_date")
    travel_class = request.args.get("travel_class")

    if not source or not destination or not journey_date:
        return jsonify({
            "status": "error",
            "message": "source, destination and journey_date are required"
        }), 400

    schedules = get_schedule_availability(
        source=source,
        destination=destination,
        journey_date=journey_date,
        travel_class=travel_class
    )

    return jsonify({
        "status": "success",
        "data_type": "database",
        "count": len(schedules),
        "schedules": schedules
    }), 200