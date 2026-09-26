import { useLocation, useNavigate } from "react-router-dom";

function BookingConfirmation() {
  const location = useLocation();
  const navigate = useNavigate();

  const { booking } = location.state || {};

  if (!booking) {
    return (
      <div className="booking-page">
        <div className="booking-container">
          <div className="no-results">

            <div className="no-results-icon">
              🎫
            </div>

            <h2>Booking not found</h2>

            <p>
              No booking information is available.
            </p>

            <button
              className="primary-button"
              onClick={() => navigate("/")}
            >
              Return Home
            </button>

          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="confirmation-page">
      <div className="confirmation-container">

        <div className="confirmation-success">

          <div className="success-icon">
            ✓
          </div>

          <span className="section-label">
            DEMONSTRATION BOOKING
          </span>

          <h1>Booking Confirmed</h1>

          <p>
            Your RailConnect demonstration booking
            has been created successfully.
          </p>

        </div>

        <div className="confirmation-card">
<div className="confirmation-top">

  <div>
    <span>PNR</span>
    <strong>{booking.pnr}</strong>
  </div>

  <div>
    <span>Booking ID</span>
    <strong>
      {booking.booking_id}
    </strong>
  </div>

  <div className="confirmed-badge">
    {booking.status}
  </div>

</div>

          <div className="confirmation-train">

            <div>
              <span>Train</span>
              <strong>{booking.train_name}</strong>
            </div>

            <div>
              <span>Train ID</span>
              <strong>{booking.train_id}</strong>
            </div>

          </div>

          <div className="confirmation-route">

            <div>
              <span>From</span>
              <strong>{booking.source}</strong>
            </div>

            <div className="confirmation-arrow">
              →
            </div>

            <div>
              <span>To</span>
              <strong>{booking.destination}</strong>
            </div>

          </div>

          <div className="confirmation-details">

            <div>
              <span>Journey Date</span>
              <strong>{booking.journey_date}</strong>
            </div>

            <div>
              <span>Travel Class</span>
              <strong>{booking.travel_class}</strong>
            </div>

            <div>
              <span>Passengers</span>
              <strong>
                {booking.passengers.length}
              </strong>
            </div>

            <div>
              <span>Total Amount</span>
              <strong>
                ₹{booking.total_amount.toLocaleString("en-IN")}
              </strong>
            </div>

          </div>

          <div className="confirmation-passengers">

            <h3>Passenger Details</h3>

            {booking.passengers.map(
              (passenger, index) => (
                <div
                  className="confirmation-passenger"
                  key={`${passenger.name}-${index}`}
                >
                  <span>
                    {index + 1}
                  </span>

                  <div>
                    <strong>
                      {passenger.name}
                    </strong>

                    <small>
                      {passenger.age} years •{" "}
                      {passenger.gender} •{" "}
                      {passenger.seat_preference}
                    </small>
                  </div>
                </div>
              )
            )}

          </div>

          <div className="confirmation-demo-note">
            This is a demonstration booking generated
            by the RailConnect Phase 1 project.
          </div>

        </div>

        <div className="confirmation-actions">

          <button
            className="primary-button"
            onClick={() => navigate("/")}
          >
            Book Another Journey
          </button>

        </div>

      </div>
    </div>
  );
}

export default BookingConfirmation;