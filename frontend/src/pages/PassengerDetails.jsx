import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

function PassengerDetails() {
  const location = useLocation();
  const navigate = useNavigate();

  const { train, journeyDate } = location.state || {};

  const [travelClass, setTravelClass] = useState(
    train?.classes?.[0] || ""
  );

  const [passenger, setPassenger] = useState({
    name: "",
    age: "",
    gender: "",
    seat_preference: "No Preference"
  });

  const [error, setError] = useState("");

  if (!train) {
    return (
      <div className="booking-page">
        <div className="booking-container">
          <div className="no-results">
            <div className="no-results-icon">🚆</div>
            <h2>Train information not found</h2>
            <p>
              Please search for a train before entering
              passenger details.
            </p>

            <button
              className="primary-button"
              onClick={() => navigate("/")}
            >
              Search Trains
            </button>
          </div>
        </div>
      </div>
    );
  }

  const handlePassengerChange = (event) => {
    const { name, value } = event.target;

    setPassenger((previous) => ({
      ...previous,
      [name]: value
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    setError("");

    if (!passenger.name.trim()) {
      setError("Please enter passenger name.");
      return;
    }

    if (!passenger.age) {
      setError("Please enter passenger age.");
      return;
    }

    if (
      Number(passenger.age) < 1 ||
      Number(passenger.age) > 120
    ) {
      setError(
        "Passenger age must be between 1 and 120."
      );
      return;
    }

    if (!passenger.gender) {
      setError("Please select passenger gender.");
      return;
    }

    navigate("/booking-summary", {
      state: {
        train,
        journeyDate,
        travelClass,
        passengers: [passenger]
      }
    });
  };

  return (
    <div className="booking-page">
      <div className="booking-container">

        <div className="booking-header">
          <span className="section-label">
            PASSENGER DETAILS
          </span>

          <h1>Complete Your Journey</h1>

          <p>
            Enter passenger information and select your
            preferred travel class.
          </p>
        </div>

        <div className="booking-layout">

          <div className="booking-form-card">

            <form onSubmit={handleSubmit}>

              <div className="form-section">
                <div className="form-section-title">
                  <span>01</span>
                  <div>
                    <h2>Travel Class</h2>
                    <p>
                      Select the class for your journey.
                    </p>
                  </div>
                </div>

                <div className="class-grid">

                  {train.classes.map((className) => (
                    <button
                      type="button"
                      key={className}
                      className={
                        travelClass === className
                          ? "class-option selected"
                          : "class-option"
                      }
                      onClick={() =>
                        setTravelClass(className)
                      }
                    >
                      <strong>{className}</strong>

                      <span>
                        {className === "1A"
                          ? "First AC"
                          : className === "2A"
                          ? "Second AC"
                          : className === "3A"
                          ? "Third AC"
                          : className === "SL"
                          ? "Sleeper"
                          : className === "CC"
                          ? "Chair Car"
                          : className === "2S"
                          ? "Second Sitting"
                          : "Available Class"}
                      </span>
                    </button>
                  ))}

                </div>
              </div>

              <div className="form-section">

                <div className="form-section-title">
                  <span>02</span>
                  <div>
                    <h2>Passenger Information</h2>
                    <p>
                      Enter details for the passenger.
                    </p>
                  </div>
                </div>

                <div className="passenger-form-grid">

                  <div className="form-field">
                    <label htmlFor="name">
                      Full Name
                    </label>

                    <input
                      id="name"
                      name="name"
                      type="text"
                      placeholder="Enter passenger name"
                      value={passenger.name}
                      onChange={handlePassengerChange}
                    />
                  </div>

                  <div className="form-field">
                    <label htmlFor="age">
                      Age
                    </label>

                    <input
                      id="age"
                      name="age"
                      type="number"
                      min="1"
                      max="120"
                      placeholder="Age"
                      value={passenger.age}
                      onChange={handlePassengerChange}
                    />
                  </div>

                  <div className="form-field">
                    <label htmlFor="gender">
                      Gender
                    </label>

                    <select
                      id="gender"
                      name="gender"
                      value={passenger.gender}
                      onChange={handlePassengerChange}
                    >
                      <option value="">
                        Select gender
                      </option>
                      <option value="Male">
                        Male
                      </option>
                      <option value="Female">
                        Female
                      </option>
                      <option value="Other">
                        Other
                      </option>
                    </select>
                  </div>

                  <div className="form-field">
                    <label htmlFor="seat_preference">
                      Seat Preference
                    </label>

                    <select
                      id="seat_preference"
                      name="seat_preference"
                      value={passenger.seat_preference}
                      onChange={handlePassengerChange}
                    >
                      <option value="No Preference">
                        No Preference
                      </option>
                      <option value="Window">
                        Window
                      </option>
                      <option value="Aisle">
                        Aisle
                      </option>
                      <option value="Lower">
                        Lower
                      </option>
                      <option value="Middle">
                        Middle
                      </option>
                      <option value="Upper">
                        Upper
                      </option>
                    </select>
                  </div>

                </div>

              </div>

              {error && (
                <div className="form-error">
                  {error}
                </div>
              )}

              <div className="booking-actions">

                <button
                  type="button"
                  className="back-button"
                  onClick={() => navigate(-1)}
                >
                  ← Back
                </button>

                <button
                  type="submit"
                  className="primary-button"
                >
                  Continue to Summary →
                </button>

              </div>

            </form>

          </div>

          <aside className="journey-card">

            <span className="section-label">
              SELECTED TRAIN
            </span>

            <h2>{train.name}</h2>

            <span className="journey-train-number">
              Train {train.train_number}
            </span>

            <div className="journey-route">

              <div>
                <strong>{train.departure}</strong>
                <span>{train.source}</span>
              </div>

              <span className="journey-arrow">
                →
              </span>

              <div>
                <strong>{train.arrival}</strong>
                <span>{train.destination}</span>
              </div>

            </div>

            <div className="journey-details">

              <div>
                <span>Journey Date</span>
                <strong>{journeyDate}</strong>
              </div>

              <div>
                <span>Duration</span>
                <strong>{train.duration}</strong>
              </div>

              <div>
                <span>Available Seats</span>
                <strong>
                  {train.available_seats}
                </strong>
              </div>

              <div>
                <span>Base Fare</span>
                <strong>
                  ₹{train.fare.toLocaleString("en-IN")}
                </strong>
              </div>

            </div>

            <div className="demo-small-note">
              Demonstration railway data
            </div>

          </aside>

        </div>

      </div>
    </div>
  );
}

export default PassengerDetails;