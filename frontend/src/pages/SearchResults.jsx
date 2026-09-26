import { useLocation, useNavigate } from "react-router-dom";

function SearchResults() {
  const location = useLocation();
  const navigate = useNavigate();

  const {
    trains = [],
    source = "",
    destination = "",
    journeyDate = ""
  } = location.state || {};

  const handleSelectTrain = (train) => {
    navigate("/passenger-details", {
      state: {
        train,
        journeyDate
      }
    });
  };

  return (
    <div className="results-page">
      <div className="results-container">

        <div className="results-header">
          <div>
            <span className="section-label">
              DEMONSTRATION TRAIN DATA
            </span>

            <h1>Available Trains</h1>

            <p>
              {source} → {destination}
              {journeyDate && ` • ${journeyDate}`}
            </p>
          </div>

          <button
            className="back-button"
            onClick={() => navigate("/")}
          >
            ← Modify Search
          </button>
        </div>

        <div className="demo-notice">
          <strong>Demo Mode:</strong>
          {" "}
          Train schedules, fares and seat availability
          shown here are demonstration data for the
          RailConnect project.
        </div>

        {trains.length === 0 ? (
          <div className="no-results">
            <div className="no-results-icon">🚆</div>
<h2>No demonstration trains found</h2>

<p>
  We could not find a demonstration train for
  {source} → {destination}.
  Try another route.
</p>

            <p>
              No demonstration train service was found
              for this route.
            </p>

            <button
              className="primary-button"
              onClick={() => navigate("/")}
            >
              Search Again
            </button>
          </div>
        ) : (
          <div className="train-list">

            {trains.map((train) => (
              <article
                className="train-card"
                key={train.id}
              >

                <div className="train-main">

                  <div className="train-info">
                    <span className="train-number">
                      {train.train_number}
                    </span>

                    <h2>{train.name}</h2>

                    <span className="train-id">
                      RailConnect ID: {train.id}
                    </span>
                  </div>

                  <div className="route-info">

                    <div className="station">
                      <strong>{train.departure}</strong>
                      <span>{train.source}</span>
                    </div>

                    <div className="route-line">
                      <span>●</span>
                      <div></div>
                      <span>●</span>
                    </div>

                    <div className="station">
                      <strong>{train.arrival}</strong>
                      <span>{train.destination}</span>
                    </div>

                  </div>

                  <div className="duration">
                    <span>Duration</span>
                    <strong>{train.duration}</strong>
                  </div>

                </div>

                <div className="train-details">

                  <div className="detail-item">
                    <span>Classes</span>
                    <strong>
                      {train.classes.join(" • ")}
                    </strong>
                  </div>

                  <div className="detail-item">
                    <span>Available Seats</span>
                    <strong className="available-seats">
                      {train.available_seats}
                    </strong>
                  </div>

                  <div className="detail-item">
                    <span>Starting Fare</span>
                    <strong>
                      ₹{train.fare.toLocaleString("en-IN")}
                    </strong>
                  </div>

                  <button
                    className="select-train-button"
                    onClick={() =>
                      handleSelectTrain(train)
                    }
                  >
                    Select Train →
                  </button>

                </div>

              </article>
            ))}

          </div>
        )}

      </div>
    </div>
  );
}

export default SearchResults;