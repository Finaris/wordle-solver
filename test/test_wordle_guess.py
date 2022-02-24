"""Tests for core components which make a Wordle guess."""

from unittest import TestCase

from wordle_solver.wordle_guess import (
    WordleGuess,
    WordleGuessComponent,
    WordleGuessComponentType,
)


class TestWordleGuessComponent(TestCase):
    """Makes sure WordleGuessComponent parsing works."""

    def test_parse(self):
        """Verifies that parsing behavior is correct."""
        # Make sure anything that's not 2 in length will raise an error.
        with self.assertRaises(AssertionError):
            WordleGuessComponent.parse("abc")
        with self.assertRaises(AssertionError):
            WordleGuessComponent.parse("a")

        # An incorrect type will also throw an error.
        with self.assertRaises(ValueError):
            WordleGuessComponent.parse("ab")
        with self.assertRaises(ValueError):
            WordleGuessComponent.parse("!a")

        # Verify that correctly formatted items parse.
        self.assertEqual(
            WordleGuessComponent.parse("a!"),
            WordleGuessComponent("a", WordleGuessComponentType.INCORRECT),
        )
        self.assertEqual(
            WordleGuessComponent.parse("b?"),
            WordleGuessComponent("b", WordleGuessComponentType.MISPLACED),
        )
        self.assertEqual(
            WordleGuessComponent.parse("c$"),
            WordleGuessComponent("c", WordleGuessComponentType.CORRECT),
        )


class TestWordleGuess(TestCase):
    """Makes sure the Wordle guesses are parsed and function correctly."""

    def test_from_user_input(self):
        """Tests that user input is parsed correctly into multiple components."""
        component_1 = WordleGuessComponent("a", WordleGuessComponentType.INCORRECT)
        component_2 = WordleGuessComponent("b", WordleGuessComponentType.CORRECT)
        expected = WordleGuess([component_1, component_2])
        result = WordleGuess.from_user_input("a! b$")
        self.assertEqual(result, expected)

    def test_iter(self):
        """Checks that iteration works as expected."""
        component_1 = WordleGuessComponent("a", WordleGuessComponentType.INCORRECT)
        component_2 = WordleGuessComponent("b", WordleGuessComponentType.CORRECT)
        expected = [component_1, component_2]
        result = list(WordleGuess(expected))
        self.assertEqual(result, expected)
