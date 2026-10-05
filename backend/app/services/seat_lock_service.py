from datetime import datetime, timedelta

from app.db import get_db_connection


LOCK_DURATION_MINUTES = 10


class SeatLockError(Exception):
    """Raised when requested seats cannot be locked."""
    pass


def lock_seats(schedule_id, seat_numbers, booking_id):
    """
    Atomically lock requested seats for an existing booking.

    Uses SELECT ... FOR UPDATE so concurrent requests cannot
    successfully lock the same seat.
    """

    if not seat_numbers:
        raise SeatLockError("At least one seat is required")

    if not booking_id:
        raise SeatLockError("booking_id is required")

    # Remove duplicates while preserving order.
    seat_numbers = list(dict.fromkeys(seat_numbers))

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:

            # 1. Release expired locks for this schedule.
            cursor.execute(
                """
                UPDATE seats
                SET
                    seat_status = 'AVAILABLE',
                    locked_until = NULL,
                    locked_by_booking_id = NULL,
                    updated_at = CURRENT_TIMESTAMP
                WHERE schedule_id = %s
                  AND seat_status = 'LOCKED'
                  AND locked_until IS NOT NULL
                  AND locked_until <= NOW()
                """,
                (schedule_id,)
            )

            # 2. Lock the requested rows.
            placeholders = ",".join(["%s"] * len(seat_numbers))

            query = f"""
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
                  AND seat_number IN ({placeholders})
                FOR UPDATE
            """

            cursor.execute(
                query,
                [schedule_id] + seat_numbers
            )

            rows = cursor.fetchall()

            # 3. Verify all requested seats exist.
            found_seats = {row["seat_number"] for row in rows}
            missing_seats = [
                seat for seat in seat_numbers
                if seat not in found_seats
            ]

            if missing_seats:
                raise SeatLockError(
                    f"Seat(s) not found: {', '.join(missing_seats)}"
                )

            # 4. Verify all requested seats are available.
            unavailable_seats = [
                row["seat_number"]
                for row in rows
                if row["seat_status"] != "AVAILABLE"
            ]

            if unavailable_seats:
                raise SeatLockError(
                    "Seat(s) not available: "
                    + ", ".join(unavailable_seats)
                )

            # 5. Calculate lock expiration.
            locked_until = datetime.now() + timedelta(
                minutes=LOCK_DURATION_MINUTES
            )

            # 6. Lock the seats.
            cursor.execute(
                f"""
                UPDATE seats
                SET
                    seat_status = 'LOCKED',
                    locked_until = %s,
                    locked_by_booking_id = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE schedule_id = %s
                  AND seat_number IN ({placeholders})
                """,
                [locked_until, booking_id, schedule_id] + seat_numbers
            )

            # 7. Commit the complete transaction.
            connection.commit()

            return {
                "schedule_id": schedule_id,
                "booking_id": booking_id,
                "seat_numbers": seat_numbers,
                "seat_status": "LOCKED",
                "locked_until": locked_until.isoformat(),
                "lock_duration_minutes": LOCK_DURATION_MINUTES
            }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()