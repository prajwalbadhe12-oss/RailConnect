import { Link } from "react-router-dom";

function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-container">

        <Link to="/" className="brand">
          <span className="brand-icon">🚆</span>

          <div>
            <span className="brand-name">
              RailConnect
            </span>

            <span className="brand-tagline">
              Smart Railway Booking
            </span>
          </div>
        </Link>

        <nav className="nav-links">
          <Link to="/">Home</Link>
          <a href="/#features">Features</a>
          <a href="/#about">About</a>
        </nav>

        <button
          className="login-button"
          type="button"
          onClick={() =>
            alert(
              "Authentication will be implemented in Phase 2."
            )
          }
        >
          Login
        </button>

      </div>
    </header>
  );
}

export default Navbar;