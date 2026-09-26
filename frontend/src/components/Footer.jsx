function Footer() {
  return (
    <footer className="footer">

      <div className="footer-container">

        <div>
          <div className="footer-brand">
            🚆 RailConnect
          </div>

          <p>
            A scalable railway ticket booking platform
            built for the RailConnect cloud project.
          </p>
        </div>

        <div>
          <h3>Platform</h3>

          <a href="/">Home</a>
          <a href="#features">Features</a>
          <a href="#about">About</a>
        </div>

        <div>
          <h3>Project</h3>

          <span>Phase 1</span>
          <span>AWS Ready</span>
          <span>Demo Railway Data</span>
        </div>

      </div>

      <div className="footer-bottom">
        <p>
          © 2026 RailConnect. Demonstration project.
        </p>
      </div>

    </footer>
  );
}

export default Footer;