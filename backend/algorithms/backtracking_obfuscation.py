"""
Backtracking Algorithm for Symbol Substitution Detection

Handles obfuscated offensive words where characters are replaced
with symbols/numbers.

Symbol Mappings:
  @ → a    1 → i, l    $ → s    0 → o    ! → i
  3 → e    4 → a       5 → s    7 → t    + → t
  . → (separator, removed)
  * → (wildcard, removed)

Approach:
  For an input like "s.t.u.p.!.d":
    1. Remove separators → "stup!d"
    2. For each character, generate possible substitutions
    3. Recursively try all combinations (backtracking)
    4. Check each generated candidate against the Trie

Time Complexity: O(2^n) in worst case (exponential due to backtracking)
  where n = length of the obfuscated word
  In practice, pruning with the Trie greatly reduces the search space.

Space Complexity: O(n) for recursion stack

Purpose: Detect heavily obfuscated offensive words that other algorithms miss.
"""

from algorithms.trie import Trie

# Character substitution mapping
SUBSTITUTIONS: dict[str, list[str]] = {
    "@": ["a"],
    "1": ["i", "l"],
    "$": ["s"],
    "0": ["o"],
    "!": ["i"],
    "3": ["e"],
    "4": ["a"],
    "5": ["s"],
    "7": ["t"],
    "+": ["t"],
    "8": ["b"],
    "9": ["g"],
    "(": ["c"],
    "|": ["l", "i"],
    "¡": ["i"],
    "€": ["e"],
    "²": ["2"],
}

# Characters that are treated as separators (removed)
SEPARATORS = {".", "-", "_", "*", "~", " "}


def normalize_text(text: str) -> str:
    """Remove separators between characters."""
    return "".join(c for c in text if c not in SEPARATORS)


def get_substitutions(char: str) -> list[str]:
    """
    Get all possible character substitutions for a given character.
    Returns the character itself plus any mapped substitutions.
    """
    result = [char.lower()]
    if char in SUBSTITUTIONS:
        result.extend(SUBSTITUTIONS[char])
    return list(set(result))


def backtrack_decode(
    obfuscated: str,
    trie: Trie,
    index: int = 0,
    current: str = "",
    results: list[str] | None = None
) -> list[str]:
    """
    Backtracking algorithm to decode obfuscated words.

    Algorithm:
      1. At each position, get all possible character substitutions
      2. Try each substitution (recursive call)
      3. If the current prefix doesn't exist in the Trie → PRUNE (backtrack)
      4. If we've processed all characters and found a word → record it

    Pruning: We use trie.starts_with() to prune branches early.
    This significantly reduces the search space from O(2^n).

    Args:
        obfuscated: The obfuscated input string
        trie: Trie containing offensive words
        index: Current position in the string
        current: Currently built candidate string
        results: Accumulator for found matches

    Returns:
        List of matched offensive words
    """
    if results is None:
        results = []

    # Base case: processed all characters
    if index == len(obfuscated):
        if trie.search(current):
            if current not in results:
                results.append(current)
        return results

    char = obfuscated[index]
    substitutions = get_substitutions(char)

    for sub in substitutions:
        candidate = current + sub

        # PRUNING: Check if any word in the Trie starts with this prefix
        # If not, backtrack immediately (don't explore this branch)
        if trie.starts_with(candidate):
            backtrack_decode(obfuscated, trie, index + 1, candidate, results)

    return results


def detect_obfuscated(text: str, trie: Trie) -> list[dict]:
    """
    Main function: detect obfuscated offensive words in text.

    Steps:
      1. Split text into tokens
      2. Normalize each token (remove separators)
      3. Apply backtracking to decode each token
      4. Collect all matches

    Args:
        text: Input text that may contain obfuscated words
        trie: Trie loaded with offensive words

    Returns:
        List of dicts with 'input', 'matched', 'method' keys
    """
    import re

    results = []
    # Split on whitespace and common separators, keeping original tokens
    tokens = re.findall(r"[a-zA-Z0-9@$!+.|_*~\-]+", text)

    for token in tokens:
        # Normalize: remove separators
        normalized = normalize_text(token)
        if len(normalized) < 2:
            continue

        # Check if it contains any substitution characters
        has_substitution = any(c in SUBSTITUTIONS or c in SEPARATORS for c in token)
        if not has_substitution:
            continue  # Skip pure alphabetic words (handled by other algorithms)

        # Apply backtracking
        matches = backtrack_decode(normalized, trie)

        for match in matches:
            # Only report if the match is different from the normalized form
            # (to avoid duplicating results from other algorithms)
            results.append({
                "input": token,
                "matched": match,
                "method": "backtracking",
                "original_token": token,
                "normalized": normalized
            })

    # Deduplicate
    seen = set()
    unique = []
    for r in results:
        key = (r["input"].lower(), r["matched"])
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return unique
