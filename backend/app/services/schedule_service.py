from datetime import time, timedelta

from app.db import get_db_connection


def _format_time(value):
    """
    Convert database TIME values into HH:MM format.

    PyMySQL may return MySQL TIME values as:
        datetime.time
        datetime.timedelta
        string
    """

    # Handle datetime.time
    if isinstance(value, time):
        return value.strftime("%H:%M")

    # Handle PyMySQL datetime.timedelta
    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())

        hours = (total_seconds // 3600) % 24
        minutes = (total_seconds % 3600) // 60

        return f"{hours:02d}:{minutes:02d}"

    # Handle string values
    value = str(value).strip()

    parts = value.split(":")

    if len(parts) >= 2:
        try:
            hour = int(parts[0])
            minute = int(parts[1])

            return f"{hour:02d}:{minute:02d}"

        except ValueError:
            pass

    return value


def _format_schedule(row):
    """
    Convert a database schedule row into
    a JSON-safe API response.
    """

    return {
        "schedule_id": row["schedule_id"],
        "journey_date": str(row["journey_date"]),
        "travel_class": row["travel_class"],
        "fare": float(row["fare"]),
        "total_seats": row["total_seats"],
        "available_seats": row["available_seats"],

        "train": {
            "id": row["train_code"],
            "train_number": row["train_number"],
            "name": row["train_name"],
            "source": row["source_station"],
            "destination": row["destination_station"],
            "departure": _format_time(row["departure_time"]),
            "arrival": _format_time(row["arrival_time"]),
            "duration": row["duration_minutes"]
        }
    }


def get_schedule_availability(
    source,
    destination,
    journey_date,
    travel_class=None
):
    """
    Retrieve train schedules and seat availability
    from the RDS database.
    """

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                SELECT
                    s.schedule_id,
                    s.journey_date,
                    s.travel_class,
                    s.fare,
                    s.total_seats,
                    s.available_seats,

                    t.train_code,
                    t.train_number,
                    t.train_name,
                    t.source_station,
                    t.destination_station,
                    t.departure_time,
                    t.arrival_time,
                    t.duration_minutes

                FROM schedules s

                INNER JOIN trains t
                    ON s.train_id = t.train_id

                WHERE t.source_station = %s
                  AND t.destination_station = %s
                  AND s.journey_date = %s
                  AND t.is_active = TRUE
            """

            params = [
                source.strip(),
                destination.strip(),
                journey_date
            ]

            if travel_class:
                query += """
                    AND s.travel_class = %s
                """

                params.append(travel_class.strip())

            query += """
                ORDER BY
                    t.departure_time,
                    s.travel_class
            """

            cursor.execute(query, params)

            rows = cursor.fetchall()

            return [
                _format_schedule(row)
                for row in rows
            ]

    finally:
        connection.close()