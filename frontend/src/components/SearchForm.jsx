
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { searchTrains } from "../services/api";

function SearchForm() {
  const navigate = useNavigate();

  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");
  const [journeyDate, setJourneyDate] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    const cleanSource = source.trim();
    const cleanDestination = destination.trim();

    // Validate station names
    if (!cleanSource || !cleanDestination) {
      setError(
        "Please enter both departure and arrival stations."
      );
      return;
    }

    // Prevent same source and destination
    if (
      cleanSource.toLowerCase() ===
      cleanDestination.toLowerCase()
    ) {
      setError(
        "Departure and arrival stations cannot be the same."
      );
      return;
    }

    // Validate journey date
    if (!journeyDate) {
      setError("Please select a journey date.");
      return;
    }

    // Prevent past journey dates
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const selectedDate = new Date(
      `${journeyDate}T00:00:00`
    );

    if (selectedDate < today) {
      setError("Journey date cannot be in the past.");
      return;
    }

    setLoading(true);

    try {
      const result = await searchTrains(
        cleanSource,
        cleanDestination
      );

      navigate("/search-results", {
        state: {
          trains: result.trains,
          source: cleanSource,
          destination: cleanDestination,
          journeyDate
        }
      });
    } catch (error) {
      console.error(error);

      setError(
        "Unable to search trains. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      className="search-form"
      onSubmit={handleSubmit}
    >
      <div className="form-field">
        <label htmlFor="source">
          From
        </label>

        <input
          id="source"
          type="text"
          placeholder="Departure station"
          value={source}
          onChange={(event) =>
            setSource(event.target.value)
          }
          required
        />
      </div>

      <div className="swap-icon">
        ⇄
      </div>

      <div className="form-field">
        <label htmlFor="destination">
          To
        </label>

        <input
          id="destination"
          type="text"
          placeholder="Arrival station"
          value={destination}
          onChange={(event) =>
            setDestination(event.target.value)
          }
          required
        />
      </div>

      <div className="form-field">
        <label htmlFor="journeyDate">
          Journey Date
        </label>

        <input
          id="journeyDate"
          type="date"
          value={journeyDate}
          onChange={(event) =>
            setJourneyDate(event.target.value)
          }
          min={
            new Date()
              .toISOString()
              .split("T")[0]
          }
          required
        />
      </div>

      <button
        type="submit"
        className="search-button"
        disabled={loading}
      >
        {loading
          ? "Searching..."
          : "Search Trains"}
      </button>

      {error && (
        <p className="search-error">
          {error}
        </p>
      )}
    </form>
  );
}

export default SearchForm;

