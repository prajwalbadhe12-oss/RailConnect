import Navbar from "../components/Navbar";
import SearchForm from "../components/SearchForm";
import Footer from "../components/Footer";


function Home() {
  return (
    <div className="app-shell">

      <Navbar />

      <main>

        {/* Hero Section */}
        <section className="hero">

          <div className="hero-overlay">

            <div className="hero-content">

              <div className="demo-badge">
                DEMONSTRATION PLATFORM
              </div>

              <h1>
                Your Journey.
                <br />
                Connected.
              </h1>

              <p>
                Search trains, explore routes and
                experience a scalable railway booking
                platform built with modern cloud
                architecture.
              </p>

            </div>

          </div>

        </section>


        {/* Search Section */}
        <section className="search-section">

          <div className="search-container">

            <div className="section-heading">

              <span className="section-label">
                PLAN YOUR JOURNEY
              </span>

              <h2>
                Find Your Train
              </h2>

              <p>
                Enter your journey details to explore
                available demonstration train services.
              </p>

            </div>

            <SearchForm />

          </div>

        </section>


        {/* Features Section */}
        <section
          className="features-section"
          id="features"
        >

          <div className="section-heading">

            <span className="section-label">
              RAILCONNECT PLATFORM
            </span>

            <h2>
              Built for Scale
            </h2>

            <p>
              This project demonstrates how a railway
              booking application can be designed for
              availability, scalability and reliability.
            </p>

          </div>


          <div className="feature-grid">

            <article className="feature-card">

              <div className="feature-icon">
                ⚡
              </div>

              <h3>
                Fast Search
              </h3>

              <p>
                Quickly search demonstration train
                schedules and routes.
              </p>

            </article>


            <article className="feature-card">

              <div className="feature-icon">
                ☁️
              </div>

              <h3>
                Cloud Ready
              </h3>

              <p>
                Designed to run on AWS with load
                balancing and auto scaling.
              </p>

            </article>


            <article className="feature-card">

              <div className="feature-icon">
                🛡️
              </div>

              <h3>
                Highly Available
              </h3>

              <p>
                Built around health checks,
                fault tolerance and scalable infrastructure.
              </p>

            </article>


            <article className="feature-card">

              <div className="feature-icon">
                📊
              </div>

              <h3>
                Infrastructure Insight
              </h3>

              <p>
                View backend server information and
                infrastructure status.
              </p>

            </article>

          </div>

        </section>


        {/* About Section */}
        <section
          className="about-section"
          id="about"
        >

          <div className="about-content">

            <span className="section-label">
              ABOUT RAILCONNECT
            </span>

            <h2>
              A Railway Booking Platform
              Designed for Real-World Scale
            </h2>

            <p>
              RailConnect is a capstone cloud project
              demonstrating a railway reservation
              application with a React frontend,
              Python Flask backend and AWS-based
              scalable infrastructure.
            </p>

            <div className="about-points">

              <span>✓ React frontend</span>
              <span>✓ Flask backend</span>
              <span>✓ AWS infrastructure</span>
              <span>✓ Auto Scaling architecture</span>

            </div>

          </div>

        </section>

      </main>

      <Footer />

    </div>
  );
}

export default Home;