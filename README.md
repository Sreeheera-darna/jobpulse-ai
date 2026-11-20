# JobPulse AI

**India Fresher Job Intelligence Platform**

A platform that collects job listings from public sources, classifies them using AI, and helps users discover relevant opportunities in India.

## Project Structure

```text
jobpulse-ai/
├── backend/
│   ├── app/
│   ├── collect_jobs.py
│   ├── classify_india_jobs.py
│   ├── india_jobs.json
│   ├── india_jobs_classified.json
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── .github/
│   └── workflows/
│       └── daily-collection.yml
└── README.md
```

## Prerequisites

- Python 3.11+
- Node.js and npm
- Gemini API key configured in `backend/.env`

## Running the Backend

Open PowerShell Terminal 1:

```powershell
cd C:\Users\darna\OneDrive\Desktop\jobpulse-ai\backend
```

Activate the Python virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Start the FastAPI server:

```powershell
python -m uvicorn app.main:app --reload
```

Backend: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

## Running the Frontend

Open a second PowerShell terminal:

```powershell
cd C:\Users\darna\OneDrive\Desktop\jobpulse-ai\frontend
```

Configure the backend URL in `frontend/.env` (copy `frontend/.env.example`):

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Install dependencies (first-time setup only):

```powershell
npm install
```

Start the React development server:

```powershell
npm run dev
```

Frontend: http://localhost:5173

## Job Data Collection

Run from the backend directory with the virtual environment activated:

```powershell
python collect_jobs.py
```

This collects job listings from configured public Greenhouse job boards, cleans duplicates, and filters India-based listings.

## AI Job Classification

Run:

```powershell
python classify_india_jobs.py
```

This uses the Gemini API to classify job listings by:

- Role category
- City
- Experience level
- Employment type
- Fresher eligibility

Classification progress is saved in `india_jobs_classified.json`, allowing the script to resume after interruptions.

## Testing the Classifier

```powershell
python test_classifier.py
```

## Useful Commands

Check Python syntax:

```powershell
python -m py_compile app/services/classifier.py
```

Stop a running server:

```text
Ctrl + C
```

## Daily Automation

GitHub Actions is configured to collect and classify jobs daily at 01:30 UTC
(07:00 India Standard Time). It commits updated JSON data to the repository.
The page also requests fresh API data every 24 hours while it remains open;
the new data becomes available after the scheduled workflow succeeds.

Workflow file:

`.github/workflows/daily-collection.yml`

The workflow requires `GEMINI_API_KEY` in the repository's Actions secrets.
The frontend deployment must set `VITE_API_BASE_URL` to the deployed backend
URL, and the backend CORS allowlist must include the deployed frontend origin.

## Current Snapshot Status

The local snapshot checked on 20 November 2026 contains 886 India-based
listings: 799 have AI classifications and 87 remain unclassified. Of the
classified rows, 33 are tagged as fresher-eligible and 18 as internships.
These counts do **not** establish 200 fresher/internship listings; do not
present the total listing count as the number of eligible opportunities.
Current-snapshot tag accuracy is also unmeasured pending the hand audit below.

## Manual Audit

The current 50-row sample is in `backend/manual_audit_50_review.csv`. Fill in its
`manual_*` fields and run the metrics script from `backend/`:

```powershell
python audit_metrics.py
```

See [AUDIT_RESULTS.md](backend/AUDIT_RESULTS.md) for the current audit status
and historical results. Historical results are not measurements of the
current sample.

## Technologies Used

**Frontend:** React, Vite, JavaScript, CSS

**Backend:** Python, FastAPI

**AI:** Google Gemini API

**Data Collection:** Public Greenhouse, Lever, and Ashby job-board APIs

**Automation:** GitHub Actions

## Security

- Store API keys in `backend/.env`.
- Never commit API keys or secrets to GitHub.
- Keep the Python virtual environment and generated temporary files out of Git.

## Project Goal

To make fresher and internship job discovery easier through automated collection, AI-powered classification, and searchable job listings.

## Quick Start

### Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload