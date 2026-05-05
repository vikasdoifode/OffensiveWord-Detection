"""
Negation Handler for Context-Aware Offensive Detection

Detects negations and reduces confidence scores for offensive words
that appear after negation words/phrases.

Common Negations:
  - Single word: not, no, don't, didn't, won't, can't, etc.
  - Phrases: "is not", "are not", "was not", "were not", etc.
  - Contractions: n't, no, never, nothing, nowhere

Algorithm: Pattern Matching + Proximity Analysis
- Time Complexity: O(n) where n = number of words
- Space Complexity: O(k) where k = number of negation words

Purpose: Reduce false positives by analyzing context around offensive words.
Examples:
  - "you are stupid" → OFFENSIVE
  - "you are not stupid" → REDUCED confidence (negation detected)
  - "I'm not being offensive" → SAFE (negation applies to whole context)
"""

import re
from typing import Tuple


class NegationHandler:
    """
    Handles negation detection to provide context-aware offensive detection.
    Reduces confidence scores when offensive words appear after negations.
    """

    # Common negation words and phrases
    NEGATION_WORDS = {
        "not", "no", "no one", "nobody", "nothing", "nowhere",
        "never", "neither", "hardly", "scarcely", "barely",
        "don't", "doesn't", "didn't", "won't", "wouldn't",
        "can't", "cannot", "couldn't", "isn't", "aren't",
        "wasn't", "weren't", "hasn't", "haven't", "hadn't",
        "shan't", "shouldn't", "mightn't", "mustn't",
        "n't",  # Contraction suffix
    }

    # Negation patterns (regex)
    NEGATION_PATTERNS = [
        r"\b(not|no|never|hardly|scarcely|barely)\b",
        r"n't\b",
        r"\b(no\s+one|nobody|nothing|nowhere|neither)\b",
    ]

    # Words that can negate sentiment
    NEGATION_INTENSIFIERS = {
        "very not", "absolutely not", "definitely not", "certainly not",
        "is not", "are not", "was not", "were not",
        "don't think", "doesn't think", "didn't think",
    }

    def __init__(self, window_size: int = 5):
        """
        Initialize the negation handler.

        Args:
            window_size: Number of words to look back for negations (default: 5)
        """
        self.window_size = window_size
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.NEGATION_PATTERNS]

    def has_negation_nearby(self, text: str, word_start: int, word_end: int) -> Tuple[bool, float]:
        """
        Check if there's a negation word/phrase near the offensive word.

        Args:
            text: Full comment text
            word_start: Start position of the offensive word
            word_end: End position of the offensive word

        Returns:
            Tuple of (has_negation, confidence_reduction_factor)
            - has_negation: True if negation detected
            - confidence_reduction_factor: How much to reduce confidence (0.0 to 1.0)
                * 0.3 = strong negation (reduce to 30% confidence)
                * 0.6 = weak negation (reduce to 60% confidence)
                * 1.0 = no negation (keep full confidence)
        """
        # Get text before the offensive word (within window)
        text_before = text[:word_start].lower()
        words_before = text_before.split()

        # Check last few words for negations
        negation_distance = 0
        for i in range(min(len(words_before), self.window_size)):
            word = words_before[-(i + 1)]  # Get word from the end
            word_clean = word.strip(".,!?;:")

            if word_clean in self.NEGATION_WORDS or any(pattern.search(word_clean) for pattern in self.compiled_patterns):
                negation_distance = i + 1
                break

        if negation_distance == 0:
            return False, 1.0  # No negation, keep full confidence

        # Calculate confidence reduction based on distance
        # Closer negation = stronger reduction
        if negation_distance == 1:
            # Negation is immediately before: "not stupid"
            reduction = 0.2  # 20% confidence (strong reduction)
        elif negation_distance <= 3:
            # Negation is 2-3 words before: "is not very stupid"
            reduction = 0.4  # 40% confidence (moderate reduction)
        else:
            # Negation is further back but within window
            reduction = 0.6  # 60% confidence (weak reduction)

        return True, reduction

    def check_question_context(self, text: str, word_start: int) -> float:
        """
        Check if the offensive word appears in a question.
        Questions are often rhetorical or not literal accusations.

        Args:
            text: Full comment text
            word_start: Start position of the offensive word

        Returns:
            Confidence factor (1.0 for statement, 0.7 for question)
        """
        # Check if there's a '?' after the word
        remaining_text = text[word_start:].lower()
        if "?" in remaining_text:
            # Check if ? comes before any period or other statement ending
            question_end = remaining_text.find("?")
            period_end = remaining_text.find(".")
            if period_end == -1 or question_end < period_end:
                return 0.7  # Reduce confidence slightly for questions
        return 1.0

    def check_irony_indicators(self, text: str) -> float:
        """
        Check for irony/sarcasm indicators that might suggest
        the offensive word is not meant literally.

        Args:
            text: Full comment text

        Returns:
            Confidence factor (1.0 for literal, 0.5 for likely ironic)
        """
        text_lower = text.lower()

        # Irony indicators
        irony_indicators = [
            "lol", "haha", "😏", "😒", "/s", "jk", "just kidding",
            "obviously", "clearly", "so", "yeah right", "sure",
            "right...", "sure buddy", "nice try"
        ]

        for indicator in irony_indicators:
            if indicator in text_lower:
                return 0.5  # Possible irony, reduce confidence

        return 1.0

    def calculate_adjusted_confidence(self, original_confidence: float, text: str, 
                                     word_start: int, word_end: int) -> float:
        """
        Calculate the adjusted confidence score considering context.

        Args:
            original_confidence: Original confidence (0.0 to 1.0)
            text: Full comment text
            word_start: Start position of the offensive word
            word_end: End position of the offensive word

        Returns:
            Adjusted confidence score (0.0 to 1.0)
        """
        # Check for negation
        has_negation, negation_factor = self.has_negation_nearby(text, word_start, word_end)

        # Check for question context
        question_factor = self.check_question_context(text, word_start)

        # Check for irony indicators
        irony_factor = self.check_irony_indicators(text)

        # Combine all factors (multiply to compound the effects)
        adjusted_confidence = original_confidence * negation_factor * question_factor * irony_factor

        return adjusted_confidence

    def get_context_explanation(self, text: str, word_start: int, word_end: int, 
                               original_confidence: float, adjusted_confidence: float) -> str:
        """
        Generate a human-readable explanation of why confidence was adjusted.

        Args:
            text: Full comment text
            word_start: Start position of the offensive word
            word_end: End position of the offensive word
            original_confidence: Original confidence
            adjusted_confidence: Adjusted confidence

        Returns:
            Explanation string
        """
        explanations = []

        # Check negation
        has_negation, _ = self.has_negation_nearby(text, word_start, word_end)
        if has_negation:
            explanations.append("Negation detected before word")

        # Check question
        if self.check_question_context(text, word_start) < 1.0:
            explanations.append("Word appears in a question")

        # Check irony
        if self.check_irony_indicators(text) < 1.0:
            explanations.append("Possible irony/sarcasm detected (lol, jk, etc.)")

        if not explanations:
            return "No context modifiers detected"

        confidence_change = (original_confidence - adjusted_confidence) * 100
        return f"{', '.join(explanations)}. Confidence reduced by {confidence_change:.1f}%"
