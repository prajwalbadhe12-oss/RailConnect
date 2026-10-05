from app.db import get_db_connection


def get_schedule_availability(
    source,
    destination,
    journey_date,
    travel_class=None
):
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
                source,
                destination,
                journey_date
            ]

            if travel_class:
                query += " AND s.travel_class = %s"
                params.append(travel_class)

            query += """
                ORDER BY
                    t.departure_time,
                    s.travel_class
            """

            cursor.execute(query, params)
            rows = cursor.fetchall()

            return rows

    finally:
        connection.close()