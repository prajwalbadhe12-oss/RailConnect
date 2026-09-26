import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { createBooking } from "../services/api";

function BookingSummary() {
  const location = useLocation();
  const navigate = useNavigate();

  const {
    train,
    journeyDate,
    travelClass,
    passengers
  } = location.state || {};

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  if (!train || !passengers || passengers.length === 0) {
    return (
      <div className="booking-page">
        <div className="booking-container">
          <div className="no-results">
            <div className="no-results-icon">🚆</div>

            <h2>Booking information not found</h2>

            <p>
              Please complete the passenger details
              before viewing the booking summary.
            </p>

            <button
              className="primary-button"
              onClick={() => navigate("/")}
            >
              Start New Search
            </button>
          </div>
        </div>
      </div>
    );
  }

  const totalAmount =
    train.fare * passengers.length;

  const handleConfirmBooking = async () => {
    setError("");
    setLoading(true);

    try {
      const result = await createBooking({
        train_id: train.id,
        journey_date: journeyDate,
        travel_class: travelClass,
        passengers
      });

      navigate("/booking-confirmation", {
        state: {
          booking: result.booking
        }
      });

    } catch (error) {
      console.error(error);

      setError(
        "Unable to create booking. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="booking-page">
      <div className="booking-container">

        <div className="booking-header">
          <span className="section-label">
            BOOKING SUMMARY
          </span>

          <h1>Review Your Booking</h1>

          <p>
            Please verify your journey and passenger
            information before confirming.
          </p>
        </div>

        <div className="summary-layout">

          <div className="summary-main">

            <section className="summary-card">

              <div className="summary-card-header">
                <div>
                  <span className="section-label">
                    JOURNEY
                  </span>

                  <h2>{train.name}</h2>
                </div>

                <span className="summary-train-number">
                  {train.train_number}
                </span>
              </div>

              <div className="summary-route">

                <div className="summary-station">
                  <span>Departure</span>
                  <strong>{train.departure}</strong>
                  <p>{train.source}</p>
                </div>

                <div className="summary-route-line">
                  <span>→</span>
                  <small>{train.duration}</small>
                </div>

                <div className="summary-station">
                  <span>Arrival</span>
                  <strong>{train.arrival}</strong>
                  <p>{train.destination}</p>
                </div>

              </div>

              <div className="summary-info-grid">

                <div>
                  <span>Journey Date</span>
                  <strong>{journeyDate}</strong>
                </div>

                <div>
                  <span>Travel Class</span>
                  <strong>{travelClass}</strong>
                </div>

                <div>
                  <span>Passengers</span>
                  <strong>{passengers.length}</strong>
                </div>

                <div>
                  <span>Booking Type</span>
                  <strong>Demo</strong>
                </div>

              </div>

            </section>

            <section className="summary-card">

              <div className="summary-card-header">
                <div>
                  <span className="section-label">
                    PASSENGERS
                  </span>

                  <h2>Passenger Details</h2>
                </div>
              </div>

              <div className="passenger-summary-list">

                {passengers.map((passenger, index) => (
                  <div
                    className="passenger-summary"
                    key={`${passenger.name}-${index}`}
                  >

                    <div className="passenger-number">
                      {index + 1}
                    </div>

                    <div className="passenger-summary-info">
                      <strong>
                        {passenger.name}
                      </strong>

                      <span>
                        {passenger.age} years •{" "}
                        {passenger.gender}
                      </span>
                    </div>

                    <div className="passenger-seat">
                      <span>Preference</span>
                      <strong>
                        {passenger.seat_preference}
                      </strong>
                    </div>

                  </div>
                ))}

              </div>

            </section>

            <div className="demo-notice">
              <strong>Demonstration Booking:</strong>{" "}
              This booking is created using RailConnect
              demo data. It does not represent a real
              railway reservation or payment.
            </div>

            {error && (
              <div className="form-error">
                {error}
              </div>
            )}

          </div>

          <aside className="fare-card">

            <span className="section-label">
              FARE SUMMARY
            </span>

            <div className="fare-row">
              <span>
                Base Fare × {passengers.length}
              </span>

              <strong>
                ₹{train.fare.toLocaleString("en-IN")}
              </strong>
            </div>

            <div className="fare-row">
              <span>Taxes & Charges</span>
              <strong>₹0</strong>
            </div>

            <div className="fare-divider"></div>

            <div className="fare-total">
              <span>Total Amount</span>

              <strong>
                ₹{totalAmount.toLocaleString("en-IN")}
              </strong>
            </div>

            <button
              className="confirm-booking-button"
              onClick={handleConfirmBooking}
              disabled={loading}
            >
              {loading
                ? "Creating Booking..."
                : "Confirm Booking →"}
            </button>

            <button
              className="summary-back-button"
              onClick={() => navigate(-1)}
              disabled={loading}
            >
              ← Edit Passenger Details
            </button>

          </aside>

        </div>

      </div>
    </div>
  );
}

export default BookingSummary;