from datetime import datetime, timedelta
import uuid

from app.db import get_db_connection


BOOKING_EXPIRATION_MINUTES = 10


class BookingDbError(Exception):
    """Raised when a database booking operation fails."""
    pass


def create_pending_booking(
    user_id,
    schedule_id,
    total_amount,
):
    """
    Create a PENDING booking in the database.

    The booking remains pending for a limited period so that
    seats can subsequently be locked against this booking.
    """

    if not user_id:
        raise BookingDbError("user_id is required")

    if not schedule_id:
        raise BookingDbError("schedule_id is required")

    if total_amount is None or total_amount < 0:
        raise BookingDbError("total_amount must be zero or greater")

    booking_reference = (
        "RC-" + uuid.uuid4().hex[:10].upper()
    )

    expires_at = (
        datetime.now()
        + timedelta(minutes=BOOKING_EXPIRATION_MINUTES)
    )

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:

            # Verify the user exists and is active.
            cursor.execute(
                """
                SELECT user_id
                FROM users
                WHERE user_id = %s
                  AND is_active = TRUE
                """,
                (user_id,)
            )

            user = cursor.fetchone()

            if user is None:
                raise BookingDbError(
                    f"Active user not found: {user_id}"
                )

            # Verify the schedule exists.
            cursor.execute(
                """
                SELECT schedule_id
                FROM schedules
                WHERE schedule_id = %s
                """,
                (schedule_id,)
            )

            schedule = cursor.fetchone()

            if schedule is None:
                raise BookingDbError(
                    f"Schedule not found: {schedule_id}"
                )

            # Create the pending booking.
            cursor.execute(
                """
                INSERT INTO bookings (
                    booking_reference,
                    user_id,
                    schedule_id,
                    booking_status,
                    total_amount,
                    expires_at
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    'PENDING',
                    %s,
                    %s
                )
                """,
                (
                    booking_reference,
                    user_id,
                    schedule_id,
                    total_amount,
                    expires_at,
                )
            )

            booking_id = cursor.lastrowid

            # Record booking status history.
            cursor.execute(
                """
                INSERT INTO booking_history (
                    booking_id,
                    old_status,
                    new_status,
                    remarks
                )
                VALUES (
                    %s,
                    NULL,
                    'PENDING',
                    %s
                )
                """,
                (
                    booking_id,
                    "Booking created and awaiting seat lock/payment",
                )
            )

            connection.commit()

            return {
                "booking_id": booking_id,
                "booking_reference": booking_reference,
                "user_id": user_id,
                "schedule_id": schedule_id,
                "booking_status": "PENDING",
                "total_amount": float(total_amount),
                "expires_at": expires_at.isoformat(),
            }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()