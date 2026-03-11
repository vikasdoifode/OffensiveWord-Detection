"""
Levenshtein Distance (Edit Distance) - Dynamic Programming Implementation

Computes the minimum number of single-character edits (insertions,
deletions, substitutions) required to change one word into another.

Time Complexity: O(m × n) where m and n are the lengths of the two strings
Space Complexity: O(m × n) for the full DP matrix, O(min(m,n)) optimized

Purpose: Detect modified/obfuscated offensive words like:
  - stup1d → stupid (distance 1)
  - f00l → fool (distance 2)
  - id10t → idiot (distance 2)

The similarity score is computed as:
  similarity = 1 - (distance / max(len(s1), len(s2)))
"""


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Compute Levenshtein distance between two strings using DP.

    Dynamic Programming recurrence:
      dp[i][j] = min(
          dp[i-1][j] + 1,        # deletion
          dp[i][j-1] + 1,        # insertion
          dp[i-1][j-1] + cost    # substitution (cost=0 if match, 1 otherwise)
      )

    Time: O(m × n)
    Space: O(m × n)
    """
    m, n = len(s1), len(s2)

    # Create DP matrix
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transforming empty string
    for i in range(m + 1):
        dp[i][0] = i  # Delete all chars from s1
    for j in range(n + 1):
        dp[0][j] = j  # Insert all chars of s2

    # Fill the DP matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1].lower() == s2[j - 1].lower():
                cost = 0
            else:
                cost = 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,      # Deletion
                dp[i][j - 1] + 1,      # Insertion
                dp[i - 1][j - 1] + cost  # Substitution
            )

    return dp[m][n]


def similarity_score(s1: str, s2: str) -> float:
    """
    Compute similarity score between two strings.
    Returns a value between 0.0 (completely different) and 1.0 (identical).
    """
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return 1.0 - (distance / max_len)


def find_similar_words(
    word: str,
    dictionary: list[str],
    threshold: float = 0.65
) -> list[dict]:
    """
    Find words in dictionary that are similar to the given word
    using Levenshtein distance.

    Args:
        word: The input word to check
        dictionary: List of known offensive words
        threshold: Minimum similarity score (0.0 - 1.0)

    Returns:
        List of dicts with 'matched', 'score', 'distance' keys
        sorted by similarity score (descending)

    Time: O(k × m × n) where k = dictionary size
    """
    results = []
    word_lower = word.lower()

    for dict_word in dictionary:
        # Skip if length difference is too large (optimization)
        if abs(len(word_lower) - len(dict_word)) > max(len(word_lower), len(dict_word)) * (1 - threshold):
            continue

        score = similarity_score(word_lower, dict_word)
        if score >= threshold:
            results.append({
                "matched": dict_word,
                "score": round(score, 3),
                "distance": levenshtein_distance(word_lower, dict_word)
            })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def get_dp_matrix(s1: str, s2: str) -> list[list[int]]:
    """
    Return the full DP matrix for visualization/debugging.
    Useful for the frontend to show the algorithm at work.
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1].lower() == s2[j - 1].lower() else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    return dp
