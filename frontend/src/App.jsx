
import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");
  const [experience, setExperience] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchJobs() {
      try {
        setLoading(true);
        setError("");

        const params = new URLSearchParams({
          search: search,
          experience: experience,
        });

        const response = await fetch(
          `http://127.0.0.1:8000/jobs?${params.toString()}`
        );

        if (!response.ok) {
          throw new Error("Could not fetch jobs from the server.");
        }

        const data = await response.json();
        setJobs(data.jobs);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchJobs();
  }, [search, experience]);

  return (
    <div className="app">
      <header className="header">
        <h1>JobPulse AI</h1>
        <p>Discover fresher jobs and internships across India</p>
      </header>

      <main className="container">
        <section className="welcome">
          <h2>Find your next opportunity.</h2>
          <p>
            Search jobs, explore roles and take the next step in your career.
          </p>
        </section>

        <section className="filters">
          <input
            type="text"
            placeholder="Search by job title, company, city or role..."
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />

          <select
            value={experience}
            onChange={(event) => setExperience(event.target.value)}
          >
            <option value="">All experience levels</option>
            <option value="Fresher">Fresher</option>
            <option value="Internship">Internship</option>
          </select>
        </section>

        <section className="results">
          <h2>Available opportunities</h2>
          <p>{jobs.length} jobs found</p>

          {loading && <p>Loading jobs...</p>}

          {error && <p className="empty">{error}</p>}

          {!loading && !error && (
            <div className="job-grid">
              {jobs.map((job) => (
                <article className="job-card" key={job.id}>
                  <span className="tag">{job.experience}</span>

{job.is_fresher_eligible === true && (
  <span className="tag fresher-tag">Fresher Eligible</span>
)}

{job.is_fresher_eligible === false && (
  <span className="tag experienced-tag">Not Fresher Eligible</span>
)}

{job.is_fresher_eligible === null && (
  <span className="tag">Not Classified</span>
)}
                  <h3>{job.title}</h3>
                  <p className="company">{job.company}</p>
                  <p>📍 {job.city}</p>
                  <p>{job.role}</p>

<a
  href={job.job_url}
  target="_blank"
  rel="noopener noreferrer"
  className="apply-button"
>
  View Job & Apply →
</a>
                </article>
              ))}
            </div>
          )}

          {!loading && !error && jobs.length === 0 && (
            <p className="empty">
              No matching jobs found. Try another search.
            </p>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;