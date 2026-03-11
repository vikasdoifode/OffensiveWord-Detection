"""
Greedy Algorithm for Offensive Word Detection

Strategy: Scan the comment from left to right and match the
LONGEST offensive word first at each position.

This is a greedy approach because:
  - At each position, we make the locally optimal choice (longest match)
  - We don't backtrack to consider shorter matches
  - This gives us fast real-time filtering

Time Complexity: O(n × m) where:
  n = length of comment
  m = length of longest offensive word

Purpose: Quick first-pass filtering before deeper analysis.
Used as a fast pre-filter in the detection pipeline.
"""

from algorithms.trie import Trie
import re


def greedy_scan(text: str, trie: Trie) -> list[dict]:
    """
    Greedy scan: at each position in the text, find the longest
    matching offensive word in the Trie.

    Algorithm:
      1. For each position i in text:
         a. Try to match the longest word starting at position i
         b. If found, record the match and skip past it
         c. If not found, move to position i+1

    This is greedy because we always take the longest match.

    Args:
        text: The input text to scan
        trie: Trie loaded with offensive words

    Returns:
        List of dicts with matched word info

    Time: O(n × m) where n = text length, m = max word length
    """
    results = []
    # Extract words from text
    words = re.findall(r"[a-zA-Z]+", text.lower())

    for word in words:
        # Try to find this exact word in the trie
        if trie.search(word):
            results.append({
                "input": word,
                "matched": word,
                "method": "greedy_exact",
                "position": text.lower().find(word)
            })
            continue

        # Greedy: try longest prefix match within the word
        i = 0
        while i < len(word):
            match = trie.find_longest_prefix_match(word, i)
            if match:
                results.append({
                    "input": word[i:i + len(match)],
                    "matched": match,
                    "method": "greedy_longest",
                    "position": i
                })
                i += len(match)  # Greedy: skip past the match
            else:
                i += 1  # No match, move forward

    # Deduplicate by matched word
    seen = set()
    unique_results = []
    for r in results:
        if r["matched"] not in seen:
            seen.add(r["matched"])
            unique_results.append(r)

    return unique_results


def greedy_word_match(text: str, offensive_words: set) -> list[dict]:
    """
    Simpler greedy approach: split text into words and check each
    against the offensive words set.

    Time: O(n) where n = number of words
    """
    results = []
    words = re.findall(r"[a-zA-Z]+", text.lower())

    for word in words:
        if word in offensive_words:
            results.append({
                "input": word,
                "matched": word,
                "method": "greedy_direct"
            })

    return results
