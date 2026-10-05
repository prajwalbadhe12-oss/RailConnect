from datetime import time, timedelta

from app.db import get_db_connection


def _format_time(value):
    """
    Convert database TIME values into HH:MM format.

    PyMySQL may return MySQL TIME values as:
        datetime.time
        datetime.timedelta
        string

    Examples:
        17:00:00 -> 17:00
        08:35:00 -> 08:35
        8:35:00  -> 08:35
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


def _format_train(row):
    """
    Convert a database train row into the API response format.
    """

    return {
        "id": row["train_code"],
        "train_number": row["train_number"],
        "name": row["train_name"],
        "source": row["source_station"],
        "destination": row["destination_station"],
        "departure": _format_time(row["departure_time"]),
        "arrival": _format_time(row["arrival_time"]),
        "duration": row["duration_minutes"],
        "data_type": "database"
    }


def get_all_trains():
    """
    Retrieve all active trains from the RDS database.
    """

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    train_code,
                    train_number,
                    train_name,
                    source_station,
                    destination_station,
                    departure_time,
                    arrival_time,
                    duration_minutes
                FROM trains
                WHERE is_active = TRUE
                ORDER BY train_id
            """)

            rows = cursor.fetchall()

            return [_format_train(row) for row in rows]

    finally:
        conn.close()


def get_train_by_id(train_id):
    """
    Retrieve a single active train using its train code.
    """

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    train_code,
                    train_number,
                    train_name,
                    source_station,
                    destination_station,
                    departure_time,
                    arrival_time,
                    duration_minutes
                FROM trains
                WHERE train_code = %s
                  AND is_active = TRUE
            """, (train_id,))

            row = cursor.fetchone()

            if row is None:
                return None

            return _format_train(row)

    finally:
        conn.close()


def search_trains(source, destination):
    """
    Search active trains by source and destination station.
    """

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    train_code,
                    train_number,
                    train_name,
                    source_station,
                    destination_station,
                    departure_time,
                    arrival_time,
                    duration_minutes
                FROM trains
                WHERE LOWER(source_station) = LOWER(%s)
                  AND LOWER(destination_station) = LOWER(%s)
                  AND is_active = TRUE
                ORDER BY train_id
            """, (source.strip(), destination.strip()))

            rows = cursor.fetchall()

            return [_format_train(row) for row in rows]

    finally:
        conn.close()