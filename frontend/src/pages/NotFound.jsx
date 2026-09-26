import { useNavigate } from "react-router-dom";

function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="booking-page">
      <div className="booking-container">

        <div className="no-results">

          <div className="no-results-icon">
            🚆
          </div>

          <span className="section-label">
            404
          </span>

          <h2>Page Not Found</h2>

          <p>
            The page you are looking for does not
            exist in the RailConnect application.
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

export default NotFound;