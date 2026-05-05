"""
Detection Engine - Orchestrates all DAA algorithms for offensive content detection.

Pipeline:
  Step 1: Greedy Scan (fast first-pass filtering)
  Step 2: Aho-Corasick (multi-pattern detection in single pass)
  Step 3: Levenshtein Distance (similarity-based detection for typos/modifications)
  Step 4: Backtracking (symbol substitution decoding)

Each step adds detected words. The final result merges all detections
and returns the overall status (OFFENSIVE / SAFE).
"""

import time
import re
from algorithms.trie import Trie
from algorithms.aho_corasick import AhoCorasick
from algorithms.levenshtein import find_similar_words
from algorithms.greedy_match import greedy_scan
from algorithms.backtracking_obfuscation import detect_obfuscated
from algorithms.negation_handler import NegationHandler


class DetectionEngine:
    """
    Central detection engine that coordinates all algorithms.
    Maintains the Trie and Aho-Corasick automaton loaded with offensive words.
    """

    def __init__(self, offensive_words: set[str]):
        self.offensive_words = offensive_words
        self.offensive_list = sorted(list(offensive_words))

        # Build Trie
        self.trie = Trie()
        for word in self.offensive_words:
            self.trie.insert(word)

        # Build Aho-Corasick automaton
        self.aho_corasick = AhoCorasick()
        for word in self.offensive_words:
            self.aho_corasick.add_pattern(word)
        self.aho_corasick.build()

        # Initialize negation handler for context-aware detection
        self.negation_handler = NegationHandler(window_size=5)

        print(f"[DetectionEngine] Loaded {len(self.offensive_words)} offensive words")
        print(f"[DetectionEngine] Trie built with {len(self.trie)} words")
        print(f"[DetectionEngine] Aho-Corasick automaton built with {len(self.aho_corasick.patterns)} patterns")
        print(f"[DetectionEngine] Negation handler initialized for context-aware detection")

    def add_word(self, word: str) -> bool:
        """Dynamically add a new offensive word."""
        word = word.lower().strip()
        if word in self.offensive_words:
            return False

        self.offensive_words.add(word)
        self.offensive_list = sorted(list(self.offensive_words))
        self.trie.insert(word)

        # Rebuild Aho-Corasick
        self.aho_corasick = AhoCorasick()
        for w in self.offensive_words:
            self.aho_corasick.add_pattern(w)
        self.aho_corasick.build()

        return True

    def analyze_comment(self, comment: str) -> dict:
        """
        Full detection pipeline for a single comment.

        Returns dict with:
          - status: "offensive" or "safe"
          - detected_words: list of detected word objects
          - algorithm_times: execution time for each algorithm
          - total_time: total detection time
        """
        all_detected = {}
        algorithm_times = {}

        # ── Step 1: Greedy Scan ──
        start = time.perf_counter()
        greedy_results = greedy_scan(comment, self.trie)
        algorithm_times["greedy"] = round((time.perf_counter() - start) * 1000, 2)

        for r in greedy_results:
            key = r["matched"]
            if key not in all_detected:
                all_detected[key] = {
                    "input": r["input"],
                    "matched": r["matched"],
                    "methods": ["greedy"],
                }

        # ── Step 2: Aho-Corasick Multi-Pattern ──
        start = time.perf_counter()
        ac_results = self.aho_corasick.search(comment)
        algorithm_times["aho_corasick"] = round((time.perf_counter() - start) * 1000, 2)

        for r in ac_results:
            key = r["word"]
            if key not in all_detected:
                all_detected[key] = {
                    "input": r["original"],
                    "matched": r["word"],
                    "methods": ["aho_corasick"],
                }
            else:
                if "aho_corasick" not in all_detected[key]["methods"]:
                    all_detected[key]["methods"].append("aho_corasick")

        # ── Step 3: Levenshtein Distance (DP) ──
        start = time.perf_counter()
        words_in_comment = re.findall(r"[a-zA-Z0-9@$!+]+", comment)
        for word in words_in_comment:
            if len(word) < 3:
                continue
            # Skip words already detected exactly
            if word.lower() in all_detected:
                continue

            similar = find_similar_words(word, self.offensive_list, threshold=0.70)
            if similar:
                best = similar[0]
                key = best["matched"]
                if key not in all_detected:
                    all_detected[key] = {
                        "input": word,
                        "matched": best["matched"],
                        "methods": ["levenshtein"],
                        "similarity": best["score"],
                        "distance": best["distance"],
                    }
                else:
                    if "levenshtein" not in all_detected[key]["methods"]:
                        all_detected[key]["methods"].append("levenshtein")
                        all_detected[key]["similarity"] = best["score"]
                        all_detected[key]["distance"] = best["distance"]

        algorithm_times["levenshtein"] = round((time.perf_counter() - start) * 1000, 2)

        # ── Step 4: Backtracking Symbol Substitution ──
        start = time.perf_counter()
        bt_results = detect_obfuscated(comment, self.trie)
        algorithm_times["backtracking"] = round((time.perf_counter() - start) * 1000, 2)

        for r in bt_results:
            key = r["matched"]
            if key not in all_detected:
                all_detected[key] = {
                    "input": r["input"],
                    "matched": r["matched"],
                    "methods": ["backtracking"],
                }
            else:
                if "backtracking" not in all_detected[key]["methods"]:
                    all_detected[key]["methods"].append("backtracking")

        # ── Compute results ──
        detected_list = list(all_detected.values())
        
        # ── Step 5: Apply Negation & Context Analysis ──
        start = time.perf_counter()
        for detected_word in detected_list:
            # Find the position of this word in the comment
            word_pos = comment.lower().find(detected_word["input"].lower())
            if word_pos != -1:
                # Calculate adjusted confidence based on context
                original_confidence = 1.0
                adjusted_confidence = self.negation_handler.calculate_adjusted_confidence(
                    original_confidence,
                    comment,
                    word_pos,
                    word_pos + len(detected_word["input"])
                )
                
                detected_word["original_confidence"] = original_confidence
                detected_word["adjusted_confidence"] = round(adjusted_confidence, 2)
                detected_word["context_explanation"] = self.negation_handler.get_context_explanation(
                    comment,
                    word_pos,
                    word_pos + len(detected_word["input"]),
                    original_confidence,
                    adjusted_confidence
                )
        
        algorithm_times["negation_context"] = round((time.perf_counter() - start) * 1000, 2)
        
        # Filter out words with very low adjusted confidence (< 0.3)
        high_confidence_words = [w for w in detected_list if w.get("adjusted_confidence", 1.0) >= 0.3]
        
        total_time = sum(algorithm_times.values())

        return {
            "comment": comment,
            "status": "offensive" if high_confidence_words else "safe",
            "detected_words": detected_list,  # Return all for transparency
            "high_confidence_detected": high_confidence_words,
            "algorithm_times": algorithm_times,
            "total_time": round(total_time, 2),
        }

    def analyze_comments_batch(self, comments: list[dict]) -> list[dict]:
        """
        Analyze a batch of comments (e.g., from YouTube chat).

        Args:
            comments: List of dicts with 'user' and 'comment' keys

        Returns:
            List of analysis results
        """
        results = []
        for item in comments:
            analysis = self.analyze_comment(item.get("comment", ""))
            results.append({
                "user": item.get("user", "Unknown"),
                "comment": item.get("comment", ""),
                "detected_words": [d["matched"] for d in analysis["detected_words"]],
                "detected_details": analysis["detected_words"],
                "status": analysis["status"],
                "algorithm_times": analysis["algorithm_times"],
                "total_time": analysis["total_time"],
            })
        return results
