"""Tests strategies used on lexicons."""

import random
from unittest import TestCase

from wordle_solver.language.lexicon_strategies import (
    CorrectLetterFilterStrategy,
    IncorrectLetterFilterStrategy,
    LengthFilterStrategy,
    MisplacedLetterFilterStrategy,
    RandomWordSelectStrategy,
    WordleGuessFilterStrategy,
)
from wordle_solver.wordle.wordle_guess import WordleGuess


class TestWordSelectStrategy(TestCase):
    """Test strategies for selecting words."""

    def test_random_word_select_strategy(self):
        """Tests strategies for randomly selecting words in the lexicon."""
        random_word_select = RandomWordSelectStrategy()
        words = {"a", "b"}
        random_word = random_word_select.select(words)
        self.assertIn(random_word, words)


class TestFilterStrategy(TestCase):
    """Tests strategies for filtering words."""

    def test_length_filter_strategy(self):
        """Checks filtering on word length is done correctly."""
        number_of_words = 10
        words = {str(i) * i for i in range(number_of_words)}
        length_filter = LengthFilterStrategy(random.randint(0, number_of_words - 1))
        filtered = length_filter.filter(words)
        result = filtered.pop()
        expected = str(len(result)) * len(result)
        self.assertEqual(result, expected)

    def test_correct_letter_filter_strategy(self):
        """Checks filtering on correct letters is done correctly."""
        words = {"ab", "ba", "cc"}
        correct_filter = CorrectLetterFilterStrategy("a", 0)
        filtered = correct_filter.filter(words)
        result = filtered.pop()
        self.assertEqual(result, "ab")

    def test_misplaced_letter_filter_strategy(self):
        """Checks filtering on misplaced letters is done correctly."""
        words = {"ab", "ba", "cc"}
        misplaced_filter = MisplacedLetterFilterStrategy("a", 0)
        result = misplaced_filter.filter(words)
        expected = {"ba", "cc"}
        self.assertSetEqual(result, expected)

    def test_incorrect_letter_filter_strategy(self):
        """Checks filtering on incorrect letters is done correctly."""
        words = {"ab", "ba", "cc"}
        incorrect_filter = IncorrectLetterFilterStrategy("a")
        filtered = incorrect_filter.filter(words)
        result = filtered.pop()
        self.assertEqual(result, "cc")

    def test_wordle_guess_filter_strategy(self):
        """Checks filtering on wordle guess feedback is done correctly."""
        words = {"dam", "dab", "add"}
        wordle_guess = WordleGuess.from_user_input("b! a$ d?")
        wordle_filter = WordleGuessFilterStrategy(wordle_guess)
        filtered = wordle_filter.filter(words)
        result = filtered.pop()
        self.assertEqual(result, "dam")
