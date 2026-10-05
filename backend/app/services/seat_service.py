from app.db import get_db_connection


def get_seats_by_schedule(schedule_id):
    """
    Retrieve all seats for a specific schedule.
    """

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    seat_id,
                    schedule_id,
                    seat_number,
                    travel_class,
                    seat_status,
                    locked_until,
                    locked_by_booking_id
                FROM seats
                WHERE schedule_id = %s
                ORDER BY seat_id
            """, (schedule_id,))

            rows = cursor.fetchall()

            seats = []

            for row in rows:
                seats.append({
                    "seat_id": row["seat_id"],
                    "schedule_id": row["schedule_id"],
                    "seat_number": row["seat_number"],
                    "travel_class": row["travel_class"],
                    "seat_status": row["seat_status"],
                    "locked_until": (
                        row["locked_until"].isoformat()
                        if row["locked_until"]
                        else None
                    ),
                    "locked_by_booking_id": row["locked_by_booking_id"]
                })

            return seats

    finally:
        connection.close()