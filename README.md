# Real-Time Offensive Comment Detection System using DAA Algorithms

A full-stack web application that detects **offensive, abusive, and obfuscated words** from user comments in real-time using multiple **Design and Analysis of Algorithms (DAA)** paradigms.

---

## 🏗️ Project Structure

```
DAA/
├── backend/
│   ├── algorithms/
│   │   ├── trie.py                    # Trie Data Structure
│   │   ├── aho_corasick.py            # Aho-Corasick Multi-Pattern Matching
│   │   ├── levenshtein.py             # Levenshtein Distance (DP)
│   │   ├── greedy_match.py            # Greedy Algorithm
│   │   └── backtracking_obfuscation.py # Backtracking Symbol Substitution
│   ├── detection/
│   │   └── detection_engine.py        # Detection Pipeline Orchestrator
│   ├── api/
│   │   └── routes.py                  # FastAPI API Routes
│   ├── utils/
│   │   └── youtube_fetcher.py         # YouTube Comment Fetcher
│   ├── dataset/
│   │   └── offensive_words.txt        # Offensive Words Dictionary
│   ├── dataset_loader.py             # Dataset Loading Utility
│   ├── main.py                       # FastAPI Entry Point
│   └── requirements.txt              # Python Dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── CommentAnalyzer.jsx
│   │   │   ├── YouTubeAnalyzer.jsx
│   │   │   ├── AlgorithmAnalysis.jsx
│   │   │   ├── AddWordPanel.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   └── PerformanceDashboard.jsx
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
└── data/
    ├── labeled_data.csv              # Labeled Dataset (26K+ tweets)
    └── readme.md
```

---

## 🚀 Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173` and the API at `http://localhost:8000`.

---

## 📊 DAA Algorithms Used

### 1. Trie Data Structure
- **Category**: Advanced Data Structure
- **Time Complexity**: O(m) insertion/search
- **Purpose**: Fast dictionary lookup for offensive words
- **Role**: Foundation for Greedy and Aho-Corasick algorithms

### 2. Aho-Corasick Algorithm
- **Category**: Pattern Matching
- **Time Complexity**: O(n + m + z)
- **Purpose**: Detect ALL offensive words in a single pass through the text
- **How**: Builds a finite state automaton with failure links

### 3. Greedy Algorithm
- **Category**: Greedy
- **Time Complexity**: O(n × m)
- **Purpose**: Fast first-pass filtering using longest-match strategy
- **How**: Scans left-to-right, always matching the longest offensive word

### 4. Levenshtein Distance (Dynamic Programming)
- **Category**: Dynamic Programming
- **Time Complexity**: O(m × n) per word pair
- **Purpose**: Detect modified/obfuscated words (e.g., "stup1d" → "stupid")
- **How**: Computes minimum edit distance using DP matrix

### 5. Backtracking Algorithm
- **Category**: Backtracking
- **Time Complexity**: O(2^n) worst case
- **Purpose**: Decode symbol substitutions (e.g., "@" → "a", "$" → "s")
- **How**: Recursively generates all possible character combinations, pruned by Trie

---

## 🔄 Detection Pipeline

```
Comment Input
    │
    ├── Step 1: Greedy Scan (fast pre-filter)
    │
    ├── Step 2: Aho-Corasick (multi-pattern match)
    │
    ├── Step 3: Levenshtein Distance (similarity check)
    │
    ├── Step 4: Backtracking (symbol substitution)
    │
    └── Result: OFFENSIVE / SAFE + detected words
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analyze-comment` | Analyze a single comment |
| POST | `/api/analyze-youtube-chat` | Analyze YouTube chat comments |
| POST | `/api/add-word` | Add new offensive word |
| GET | `/api/words` | Get all offensive words |
| GET | `/api/algorithms` | Get algorithm analysis info |
| GET | `/api/health` | Health check |

### Example: Analyze Comment

**Request:**
```json
POST /api/analyze-comment
{
  "comment": "You are stup1d and id10t"
}
```

**Response:**
```json
{
  "comment": "You are stup1d and id10t",
  "status": "offensive",
  "detected_words": [
    {"input": "stup1d", "matched": "stupid", "methods": ["backtracking", "levenshtein"], "similarity": 0.833},
    {"input": "id10t", "matched": "idiot", "methods": ["levenshtein"], "similarity": 0.6}
  ],
  "algorithm_times": {
    "greedy": 0.12,
    "aho_corasick": 0.08,
    "levenshtein": 5.43,
    "backtracking": 1.21
  },
  "total_time": 6.84
}
```

---

## 🎨 Frontend Features

- **Dark Mode** modern AI moderation dashboard
- **Comment Analyzer** with real-time detection
- **YouTube Chat Analyzer** with table view
- **DAA Analysis Page** with algorithm comparison
- **Dictionary Manager** to add/browse words
- **Performance Dashboard** showing algorithm execution times
- **Offensive word highlighting** in red
- **Responsive layout** for all screen sizes

---

## 📁 Dataset

The project uses the `labeled_data.csv` dataset containing 26,000+ tweets classified as:
- **Class 0**: Hate Speech
- **Class 1**: Offensive Language
- **Class 2**: Neither

The base offensive words dictionary (`offensive_words.txt`) contains curated offensive words used for detection.

---

## 🔧 Configuration

### YouTube API (Optional)
Set the `YOUTUBE_API_KEY` environment variable to use real YouTube comments:
```bash
set YOUTUBE_API_KEY=your_api_key_here
```

Without an API key, the system uses simulated chat data for demonstration.

---

## 📈 Performance

The system provides real-time performance metrics for each algorithm:
- **Greedy Scan**: ~0.1ms
- **Aho-Corasick**: ~0.1ms
- **Levenshtein**: ~2-10ms (depends on word count)
- **Backtracking**: ~0.5-5ms (depends on obfuscation)

Total detection time is typically under 15ms per comment.
