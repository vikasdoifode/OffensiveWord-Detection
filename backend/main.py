"""
Real-Time Offensive Comment Detection System using DAA Algorithms

Main FastAPI application entry point.

Run with:
  uvicorn main:app --reload --port 8000

This system uses multiple DAA algorithm paradigms:
  1. Trie Data Structure - Fast dictionary lookup
  2. Aho-Corasick Algorithm - Multi-pattern matching
  3. Greedy Algorithm - Fast scanning with longest match
  4. Levenshtein Distance (DP) - Similarity detection
  5. Backtracking - Symbol substitution decoding
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the backend directory (same directory as main.py)
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("YOUTUBE_API_KEY", "")
print(f"[Debug] .env path: {env_path} (exists: {env_path.exists()})")
print(f"[Debug] YOUTUBE_API_KEY loaded: {'YES (' + api_key[:10] + '...)' if api_key else 'NO — YouTube will use simulated data'}")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router, set_engine
from detection.detection_engine import DetectionEngine
from dataset_loader import load_all_offensive_words

# ── Create FastAPI App ──
app = FastAPI(
    title="Real-Time Offensive Comment Detection System",
    description="Detect offensive, abusive, and obfuscated words using DAA algorithms",
    version="1.0.0",
)

# ── CORS Middleware (allow React frontend) ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Initialize Detection Engine on Startup ──
@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("  Real-Time Offensive Comment Detection System")
    print("  Using DAA Algorithms")
    print("=" * 60)

    # Load offensive words
    offensive_words = load_all_offensive_words()
    print(f"\n[Startup] Loaded {len(offensive_words)} offensive words from dataset")

    # Initialize detection engine
    engine = DetectionEngine(offensive_words)
    set_engine(engine)

    print("\n[Startup] Detection engine initialized successfully!")
    print("[Startup] API is ready at http://localhost:8000")
    print("[Startup] Docs available at http://localhost:8000/docs")
    print("=" * 60)


# ── Include API routes ──
app.include_router(router, prefix="/api")


# ── Root endpoint ──
@app.get("/")
async def root():
    return {
        "message": "Real-Time Offensive Comment Detection System",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "analyze_comment": "POST /api/analyze-comment",
            "analyze_youtube": "POST /api/analyze-youtube-chat",
            "add_word": "POST /api/add-word",
            "get_words": "GET /api/words",
            "health": "GET /api/health",
            "algorithms": "GET /api/algorithms",
        },
    }
