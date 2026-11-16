
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.jobs import router as jobs_router

app = FastAPI(
    title="JobPulse AI",
    description="India Fresher Job Intelligence Platform",
    version="1.0.0"
)

# Allow the React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to JobPulse AI",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "JobPulse AI Backend"
    }