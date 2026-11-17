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

GitHub Actions is configured to run the job collection workflow daily.

Workflow file:

`.github/workflows/daily-collection.yml`

## Technologies Used

**Frontend:** React, Vite, JavaScript, CSS

**Backend:** Python, FastAPI

**AI:** Google Gemini API

**Data Collection:** Greenhouse Public Job Board API

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