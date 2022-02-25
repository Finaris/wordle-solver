"""Tests for lexicon representation."""

from os.path import abspath, dirname
from pathlib import Path
from unittest import TestCase

from wordle_solver.language.lexicon import EnglishLexicon


class TestLexicon(TestCase):
    """Check all functions on the lexicon."""

    def test_length(self):
        """Makes sure the length is calculated correctly."""
        lexicon = EnglishLexicon({"a", "b"})
        self.assertEqual(lexicon.length, 2)
        lexicon.words.pop()
        self.assertEqual(lexicon.length, 1)

    def test_from_file(self):
        """Checks that reading from a file works correctly."""
        this_dir = dirname(abspath(__file__))
        test_words = this_dir / Path("data") / Path("words.txt")
        lexicon = EnglishLexicon.from_file(test_words)
        expected = {"this", "is", "a", "test"}
        self.assertEqual(lexicon.words, expected)

    def test_sample(self):
        """Checks that sampling is done correctly."""
        # TODO

    def test_filter(self):
        """Checks that filtering works correctly."""
        # TODO

    def test_discard(self):
        """Validates discarding behavior for lexicons."""
        lexicon = EnglishLexicon({"a", "b"})
        self.assertFalse(lexicon.discard("c"))
        self.assertTrue(lexicon.discard("a"))
