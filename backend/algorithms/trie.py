"""
Trie Data Structure Implementation for DAA Project

Time Complexity:
  - Insertion: O(m) where m = length of word
  - Search: O(m) where m = length of word
  - Prefix Search: O(m)

Space Complexity: O(ALPHABET_SIZE * m * n) where n = number of words

Purpose: Fast dictionary lookup for offensive words.
Used as the foundation for Greedy matching and Aho-Corasick.
"""


class TrieNode:
    """A node in the Trie data structure."""

    __slots__ = ["children", "is_end_of_word", "word"]

    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_end_of_word: bool = False
        self.word: str = ""


class Trie:
    """
    Trie (Prefix Tree) Data Structure

    Supports:
    - Insert word: O(m)
    - Search word: O(m)
    - Prefix check: O(m)
    - Get all words with prefix: O(m + k) where k = number of matching words
    """

    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0

    def insert(self, word: str) -> None:
        """Insert a word into the Trie. Time: O(m), Space: O(m)"""
        node = self.root
        word_lower = word.lower().strip()
        for char in word_lower:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        if not node.is_end_of_word:
            node.is_end_of_word = True
            node.word = word_lower
            self.word_count += 1

    def search(self, word: str) -> bool:
        """Search for a word in the Trie. Time: O(m)"""
        node = self._traverse(word.lower().strip())
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Check if any word starts with given prefix. Time: O(m)"""
        return self._traverse(prefix.lower().strip()) is not None

    def _traverse(self, text: str) -> TrieNode | None:
        """Traverse the Trie following the characters in text."""
        node = self.root
        for char in text:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def get_all_words(self) -> list[str]:
        """Get all words stored in the Trie."""
        words = []
        self._collect_words(self.root, words)
        return words

    def _collect_words(self, node: TrieNode, words: list[str]) -> None:
        """DFS to collect all words from the Trie."""
        if node.is_end_of_word:
            words.append(node.word)
        for child in node.children.values():
            self._collect_words(child, words)

    def find_longest_prefix_match(self, text: str, start: int) -> str | None:
        """
        From position `start` in text, find the longest word in the Trie
        that matches. Used by the Greedy algorithm.
        Time: O(m) where m = length of longest word
        """
        node = self.root
        longest_match = None
        for i in range(start, len(text)):
            char = text[i].lower()
            if char not in node.children:
                break
            node = node.children[char]
            if node.is_end_of_word:
                longest_match = node.word
        return longest_match

    def __len__(self) -> int:
        return self.word_count

    def __contains__(self, word: str) -> bool:
        return self.search(word)
