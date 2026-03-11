"""
Aho-Corasick Algorithm Implementation for DAA Project

Multi-pattern string matching algorithm that finds all occurrences
of a set of patterns in a text in a single pass.

Time Complexity:
  - Build automaton: O(sum of pattern lengths)
  - Search: O(n + m + z) where:
      n = text length
      m = total pattern length
      z = number of matches

Space Complexity: O(sum of pattern lengths * ALPHABET_SIZE)

Purpose: Detect multiple offensive words in a single pass through the comment.
This is significantly faster than searching for each word individually.
"""

from collections import deque


class AhoCorasickNode:
    """Node in the Aho-Corasick automaton."""

    __slots__ = ["children", "fail", "output", "depth"]

    def __init__(self):
        self.children: dict[str, "AhoCorasickNode"] = {}
        self.fail: "AhoCorasickNode | None" = None
        self.output: list[str] = []
        self.depth: int = 0


class AhoCorasick:
    """
    Aho-Corasick Automaton for multi-pattern matching.

    Build Phase:
      1. Construct a Trie from all patterns
      2. Build failure links using BFS (similar to KMP failure function)
      3. Build output links for collecting all matches

    Search Phase:
      - Process text character by character
      - Follow failure links on mismatch
      - Collect all pattern matches at each state
    """

    def __init__(self):
        self.root = AhoCorasickNode()
        self.patterns: list[str] = []
        self._built = False

    def add_pattern(self, pattern: str) -> None:
        """Add a pattern to the automaton. Must call build() after adding all patterns."""
        pattern = pattern.lower().strip()
        if not pattern:
            return
        self.patterns.append(pattern)
        node = self.root
        for char in pattern:
            if char not in node.children:
                node.children[char] = AhoCorasickNode()
                node.children[char].depth = node.depth + 1
            node = node.children[char]
        node.output.append(pattern)
        self._built = False

    def build(self) -> None:
        """
        Build the failure links using BFS.
        Time: O(sum of all pattern lengths)

        The failure link of a node points to the longest proper suffix
        of the string represented by that node, which is also a prefix
        of some pattern in the automaton.
        """
        queue = deque()

        # Initialize failure links for depth-1 nodes
        for char, child in self.root.children.items():
            child.fail = self.root
            queue.append(child)

        # BFS to build failure links
        while queue:
            current = queue.popleft()

            for char, child in current.children.items():
                queue.append(child)

                # Follow failure links to find the longest proper suffix
                fail_node = current.fail
                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.fail

                child.fail = fail_node.children[char] if fail_node and char in fail_node.children else self.root

                # Merge output - if fail node has outputs, add them
                if child.fail and child.fail != child:
                    child.output = child.output + child.fail.output

        self._built = True

    def search(self, text: str) -> list[dict]:
        """
        Search for all pattern occurrences in text.
        Time: O(n + z) where n = len(text), z = number of matches

        Returns list of dicts with 'word', 'start', 'end' keys.
        """
        if not self._built:
            self.build()

        results = []
        node = self.root
        text_lower = text.lower()

        for i, char in enumerate(text_lower):
            # Follow failure links until we find a match or reach root
            while node is not None and char not in node.children:
                node = node.fail if node.fail else self.root
                if node == self.root and char not in node.children:
                    break

            if char in node.children:
                node = node.children[char]
            else:
                node = self.root
                continue

            # Collect all matches at current position
            for pattern in node.output:
                start = i - len(pattern) + 1
                results.append({
                    "word": pattern,
                    "start": start,
                    "end": i + 1,
                    "original": text[start:i + 1]
                })

        return results

    def search_words(self, text: str) -> list[str]:
        """Return just the matched words (deduplicated)."""
        matches = self.search(text)
        return list(set(m["word"] for m in matches))
