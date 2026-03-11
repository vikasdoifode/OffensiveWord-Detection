"""
API Routes for Offensive Comment Detection System

Endpoints:
  POST /analyze-comment     - Analyze a single comment
  POST /analyze-youtube-chat - Analyze YouTube chat comments
  POST /add-word            - Add a new offensive word
  GET  /words               - Get all offensive words
  GET  /health              - Health check
  GET  /algorithms          - Get algorithm analysis info
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from detection.detection_engine import DetectionEngine
from utils.youtube_fetcher import fetch_youtube_comments

router = APIRouter()

# Global engine instance (set by main.py)
engine: DetectionEngine | None = None


def set_engine(e: DetectionEngine):
    global engine
    engine = e


# ── Request/Response Models ──

class CommentRequest(BaseModel):
    comment: str


class YouTubeRequest(BaseModel):
    url: str


class AddWordRequest(BaseModel):
    word: str


class DetectedWord(BaseModel):
    input: str
    matched: str
    methods: list[str] = []
    similarity: float | None = None
    distance: int | None = None


class CommentResponse(BaseModel):
    comment: str
    status: str
    detected_words: list[dict]
    algorithm_times: dict
    total_time: float


class YouTubeChatResponse(BaseModel):
    comments: list[dict]
    total_analyzed: int
    offensive_count: int
    safe_count: int
    source: str = "unknown"


# ── Endpoints ──

@router.post("/analyze-comment", response_model=CommentResponse)
async def analyze_comment(request: CommentRequest):
    """
    Analyze a single comment for offensive content.

    Uses all DAA algorithms in sequence:
    1. Greedy Scan
    2. Aho-Corasick Multi-Pattern Matching
    3. Levenshtein Distance (DP)
    4. Backtracking Symbol Substitution
    """
    if not engine:
        raise HTTPException(status_code=500, detail="Detection engine not initialized")

    if not request.comment.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    result = engine.analyze_comment(request.comment)
    return result


@router.post("/analyze-youtube-chat", response_model=YouTubeChatResponse)
async def analyze_youtube_chat(request: YouTubeRequest):
    """
    Fetch and analyze YouTube chat/video comments.

    1. Fetches comments from YouTube (or simulated data)
    2. Runs each comment through the full detection pipeline
    3. Returns analysis results for all comments
    """
    if not engine:
        raise HTTPException(status_code=500, detail="Detection engine not initialized")

    if not request.url.strip():
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    # Fetch comments
    comments, source = await fetch_youtube_comments(request.url)

    if not comments:
        raise HTTPException(status_code=404, detail="No comments found")

    # Analyze all comments
    results = engine.analyze_comments_batch(comments)

    offensive_count = sum(1 for r in results if r["status"] == "offensive")
    safe_count = sum(1 for r in results if r["status"] == "safe")

    return {
        "comments": results,
        "total_analyzed": len(results),
        "offensive_count": offensive_count,
        "safe_count": safe_count,
        "source": source,
    }


@router.post("/add-word")
async def add_word(request: AddWordRequest):
    """
    Dynamically add a new offensive word to the detection system.
    Updates the Trie and rebuilds the Aho-Corasick automaton.
    """
    if not engine:
        raise HTTPException(status_code=500, detail="Detection engine not initialized")

    word = request.word.strip().lower()
    if not word:
        raise HTTPException(status_code=400, detail="Word cannot be empty")

    if len(word) < 2:
        raise HTTPException(status_code=400, detail="Word must be at least 2 characters")

    added = engine.add_word(word)
    if added:
        return {"status": "success", "message": f"Word '{word}' added successfully", "total_words": len(engine.offensive_words)}
    else:
        return {"status": "exists", "message": f"Word '{word}' already exists", "total_words": len(engine.offensive_words)}


@router.get("/words")
async def get_words():
    """Get all offensive words in the dictionary."""
    if not engine:
        raise HTTPException(status_code=500, detail="Detection engine not initialized")

    return {
        "words": sorted(list(engine.offensive_words)),
        "total": len(engine.offensive_words),
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "engine_loaded": engine is not None,
        "total_words": len(engine.offensive_words) if engine else 0,
    }


@router.get("/algorithms")
async def get_algorithms():
    """Get algorithm analysis information for the DAA Analysis page."""
    return {
        "algorithms": [
            {
                "name": "Trie Data Structure",
                "category": "Advanced Data Structure",
                "time_complexity": "O(m)",
                "space_complexity": "O(ALPHABET × m × n)",
                "purpose": "Fast dictionary lookup and prefix matching for offensive words",
                "description": "A tree-like data structure where each node represents a character. Words are stored as paths from root to leaf. Enables O(m) lookups where m is the word length.",
                "used_in": "Foundation for Greedy and Aho-Corasick algorithms",
            },
            {
                "name": "Aho-Corasick Algorithm",
                "category": "Pattern Matching",
                "time_complexity": "O(n + m + z)",
                "space_complexity": "O(m × ALPHABET)",
                "purpose": "Multi-pattern matching - detect all offensive words in a single pass",
                "description": "Builds a finite state automaton from all patterns. Uses failure links (similar to KMP) to efficiently match multiple patterns simultaneously. Processes the entire text in one pass.",
                "used_in": "Step 2 of detection pipeline",
            },
            {
                "name": "Greedy Algorithm",
                "category": "Greedy",
                "time_complexity": "O(n × m)",
                "space_complexity": "O(1)",
                "purpose": "Fast first-pass scanning using longest match strategy",
                "description": "Scans text from left to right, always matching the longest offensive word at each position. Makes locally optimal choices without backtracking.",
                "used_in": "Step 1 of detection pipeline (fast pre-filter)",
            },
            {
                "name": "Levenshtein Distance",
                "category": "Dynamic Programming",
                "time_complexity": "O(m × n)",
                "space_complexity": "O(m × n)",
                "purpose": "Detect modified/obfuscated words through similarity matching",
                "description": "Computes the minimum edit distance between two strings using a DP matrix. Detects words with character substitutions, insertions, or deletions (e.g., 'stup1d' → 'stupid').",
                "used_in": "Step 3 of detection pipeline",
            },
            {
                "name": "Backtracking Algorithm",
                "category": "Backtracking",
                "time_complexity": "O(2^n)",
                "space_complexity": "O(n)",
                "purpose": "Decode symbol substitutions through recursive exploration",
                "description": "Recursively generates all possible character combinations from symbol-substituted text. Uses Trie-based pruning to reduce the exponential search space. Handles mappings like @ → a, $ → s, ! → i.",
                "used_in": "Step 4 of detection pipeline",
            },
        ],
        "pipeline": [
            {"step": 1, "algorithm": "Greedy Scan", "description": "Quick first-pass filtering using longest match"},
            {"step": 2, "algorithm": "Aho-Corasick", "description": "Multi-pattern detection in single pass"},
            {"step": 3, "algorithm": "Levenshtein (DP)", "description": "Similarity-based detection for modified words"},
            {"step": 4, "algorithm": "Backtracking", "description": "Symbol substitution decoding"},
        ],
        "paradigms": [
            "Greedy Algorithms",
            "Dynamic Programming",
            "Backtracking",
            "Advanced Data Structures (Trie)",
            "Pattern Matching (Aho-Corasick)",
        ],
    }
