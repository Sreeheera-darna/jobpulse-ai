
import { useState, useEffect } from "react";
import "./App.css";

const DAILY_REFRESH_MS = 24 * 60 * 60 * 1000;

function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");
  const [experience, setExperience] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [theme, setTheme] = useState(
    () => localStorage.getItem("jobpulse-theme") || "light"
  );

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("jobpulse-theme", theme);
  }, [theme]);

  useEffect(() => {
    async function fetchJobs() {
      try {
        setLoading(true);
        setError("");

        const params = new URLSearchParams({
          search,
          experience,
        });

        const response = await fetch(
          `${import.meta.env.VITE_API_BASE_URL}/jobs?${params.toString()}`
        );

        if (!response.ok) {
          throw new Error("Could not fetch jobs from the server.");
        }

        const data = await response.json();
        setJobs(data.jobs || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchJobs();
    const refreshInterval = window.setInterval(fetchJobs, DAILY_REFRESH_MS);

    return () => window.clearInterval(refreshInterval);
  }, [search, experience]);

  const fresherCount = jobs.filter(
    (job) => job.is_fresher_eligible === true
  ).length;

  const internshipCount = jobs.filter(
    (job) =>
      (job.experience || "").toLowerCase().includes("intern")
  ).length;

  const isDark = theme === "dark";

  return (
    <div className="app-shell">

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">J</div>
          <span>JobPulse<span className="brand-ai"> AI</span></span>
        </div>

        <div className="nav-label">WORKSPACE</div>

        <nav className="navigation">
          <a href="#dashboard" className="nav-link active">
            <span>▦</span> Dashboard
          </a>

          <a href="#jobs" className="nav-link">
            <span>⌕</span> Explore Jobs
          </a>

          <button
            className="nav-link nav-button"
            onClick={() => setExperience("Fresher")}
          >
            <span>✦</span> Fresher Jobs
          </button>

          <button
            className="nav-link nav-button"
            onClick={() => setExperience("Internship")}
          >
            <span>◷</span> Internships
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-note">
            <span className="note-icon">✦</span>
            <strong>Your next opportunity starts here.</strong>
            <p>Discover opportunities and move your career forward.</p>
          </div>
          <p className="sidebar-version">JOBPULSE AI · INDIA</p>
        </div>
      </aside>

      <main className="main-area" id="dashboard">

        <header className="topbar">
          <div>
            <p className="breadcrumb">Workspace / Dashboard</p>
            <h2>Dashboard</h2>
          </div>

          <button
            className="theme-toggle"
            onClick={() => setTheme(isDark ? "light" : "dark")}
            aria-label={`Switch to ${isDark ? "light" : "dark"} mode`}
          >
            <span>{isDark ? "☀" : "☾"}</span>
            {isDark ? "Light Mode" : "Dark Mode"}
          </button>
        </header>

        <div className="dashboard-content">

          <section className="hero">
            <div className="hero-content">
              <span className="hero-eyebrow">YOUR CAREER, YOUR NEXT MOVE</span>
              <h1>Find work that moves you forward.</h1>
              <p>
                Explore fresher opportunities, internships and jobs
                from companies across India.
              </p>
              <a href="#jobs" className="hero-button">
                Explore opportunities <span>→</span>
              </a>
            </div>
            <div className="hero-decoration">✦</div>
          </section>

          <section className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon purple">▦</div>
              <p>Total matching jobs</p>
              <h3>{jobs.length}</h3>
              <span>Opportunities available</span>
            </div>

            <div className="stat-card">
              <div className="stat-icon green">✦</div>
              <p>Fresher eligible</p>
              <h3>{fresherCount}</h3>
              <span>Open to fresh graduates</span>
            </div>

            <div className="stat-card">
              <div className="stat-icon orange">◷</div>
              <p>Internships</p>
              <h3>{internshipCount}</h3>
              <span>Internship opportunities</span>
            </div>
          </section>

          <section className="jobs-section" id="jobs">
            <div className="section-heading">
              <div>
                <span className="section-eyebrow">OPPORTUNITY BOARD</span>
                <h2>Explore opportunities</h2>
                <p>Find the right role for your next career move.</p>
              </div>
              <span className="jobs-count">{jobs.length} jobs found</span>
            </div>

            <div className="filters">
              <div className="search-box">
                <span>⌕</span>
                <input
                  type="text"
                  placeholder="Search job title, company or city..."
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                />
              </div>

              <select
                value={experience}
                onChange={(event) => setExperience(event.target.value)}
              >
                <option value="">All experience levels</option>
                <option value="Fresher">Fresher</option>
                <option value="Internship">Internship</option>
              </select>
            </div>

            {loading && (
              <div className="message-card">Loading opportunities...</div>
            )}

            {error && (
              <div className="message-card error-message">{error}</div>
            )}

            {!loading && !error && (
              <div className="job-grid">
                {jobs.map((job) => (
                  <article className="job-card" key={job.id}>

                    <div className="job-card-top">
                      <div className="company-avatar">
                        {(job.company || "J").charAt(0).toUpperCase()}
                      </div>

                      <span className="job-category">
                        {job.role || "Other"}
                      </span>
                    </div>

                    <div className="job-company">{job.company}</div>

                    <h3>{job.title}</h3>

                    <div className="job-details">
                      <span>⌖ {job.city || "India"}</span>
                      <span>◷ {job.experience || "Not specified"}</span>
                    </div>

                    <div className="job-badges">
                      {job.is_fresher_eligible === true && (
                        <span className="badge fresher-badge">
                          Fresher Eligible
                        </span>
                      )}

                      {job.is_fresher_eligible === false && (
                        <span className="badge experienced-badge">
                          Experienced
                        </span>
                      )}

                      {job.is_fresher_eligible === null && (
                        <span className="badge unknown-badge">
                          Not Classified
                        </span>
                      )}
                    </div>

                    <a
                      href={job.job_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="apply-button"
                    >
                      View job details <span>→</span>
                    </a>

                  </article>
                ))}
              </div>
            )}

            {!loading && !error && jobs.length === 0 && (
              <div className="message-card">
                No matching jobs found. Try another search.
              </div>
            )}
          </section>

          <footer className="footer">
            <span>© 2026 JobPulse AI</span>
            <span>Built to help you discover your next opportunity.</span>
          </footer>

        </div>
      </main>
    </div>
  );
}
export default App;
