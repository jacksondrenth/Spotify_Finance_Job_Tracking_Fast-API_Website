from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database import engine, Base
import models

load_dotenv()

# Create all database tables defined in models.py
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Dashboard API", version="1.0.0")

# CORS middleware - Enforcing Security Policy
app.add_middleware(
    CORSMiddleware,
    allow_orgins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and register routers
from routers import spotify, finance, jobs

# Each module has own routing file
app.include_router(spotify.router, prefix="/api/spotify", tags=["spotify"])
app.include_router(finance.router, prefix="/api/finance", tags=["finance"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])

@app.get("/")
def root():
    return {"status": "Personal Dashboard API is running"}