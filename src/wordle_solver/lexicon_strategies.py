"""Strategies for working with data contained in lexicons."""

import random
from abc import ABC, abstractmethod
from collections import Counter
from typing import Set

from wordle_solver.wordle.wordle_guess import WordleGuess, WordleGuessComponentType


class WordSelectStrategy(ABC):
    """A strategy for selecting words from a lexicon."""

    @abstractmethod
    def select(self, words: Set[str]) -> str:
        """Selects a word from the provided lexicon.

        :param words: a set of words
        :return: a word from the set
        """
        ...


class RandomWordSelectStrategy(WordSelectStrategy):
    """Selects a word randomly."""

    def select(self, words: Set[str]) -> str:
        """Randomly selects a word from the set.

        :param words: a set of words
        :return: a word from the set
        """
        return random.choice(tuple(words))


class FilterStrategy(ABC):
    """Filters a lexicon."""

    @abstractmethod
    def filter(self, words: Set[str]) -> Set[str]:
        """Filters the provided set of words.

        :param words: initial set of words to filter
        :return: filtered set of words
        """
        ...


class LengthFilterStrategy(FilterStrategy):
    """Filters based on length."""

    def __init__(self, length: int):
        """Determines length to filter by.

        :param length: length to filter by
        """
        self.length: int = length

    def filter(self, words: Set[str]) -> Set[str]:
        """Filters words on length.

        :param words: initial set of words to filter
        :return: filtered set of words
        """
        return set(filter(lambda w: len(w) == self.length, words))


class CorrectLetterFilterStrategy(FilterStrategy):
    """Filter using a correct letter in a position."""

    def __init__(self, letter: str, index: int):
        """Creates a filter using a correct letter at the given index.

        :param letter: the correct letter
        :param index: index which this letter is correct at
        """
        assert len(letter) == 1, f"expected {letter} to be a single letter"
        self.letter: str = letter
        self.index: int = index

    def filter(self, words: Set[str]) -> Set[str]:
        """Filters words by setting correct letters.

        :param words: initial set of words to filter
        :return: filtered set of words
        """
        correct_length_words = set(filter(lambda w: len(w) >= self.index, words))
        return set(filter(lambda w: w[self.index] == self.letter, correct_length_words))


class MisplacedLetterFilterStrategy(FilterStrategy):
    """Filter using a letter in the word but incorrect position."""

    def __init__(self, letter: str, index: int):
        """Creates a filter using a misplaced letter at the given index.

        :param letter: the misplaced letter
        :param index: index which this letter is misplaced at
        """
        assert len(letter) == 1, f"expected {letter} to be a single letter"
        self.letter: str = letter
        self.index: int = index

    def filter(self, words: Set[str]) -> Set[str]:
        """Filters words by removing misplaced letters at a position.

        :param words: initial set of words to filter
        :return: filtered set of words
        """
        correct_length_words = set(filter(lambda w: len(w) >= self.index, words))
        return set(filter(lambda w: w[self.index] != self.letter, correct_length_words))


class IncorrectLetterFilterStrategy(FilterStrategy):
    """Filter using a correct letter in a position."""

    def __init__(self, letter: str):
        """Creates filter which removes the provided letter.

        :param letter: letter to remove
        """
        assert len(letter) == 1, f"expected {letter} to be a single letter"
        self.letter: str = letter

    def filter(self, words: Set[str]) -> Set[str]:
        """Filters words by removing incorrect letters.

        :param words: initial set of words to filter
        :return: filtered set of words
        """
        return set(filter(lambda w: self.letter not in w, words))


class WordleGuessFilterStrategy(FilterStrategy):
    """Filters using a Wordle guess."""

    def __init__(self, wordle_guess: WordleGuess):
        """Creates filter which will use the given Wordle guess

        :param wordle_guess: WordleGuess to filter by
        """
        self.wordle_guess: WordleGuess = wordle_guess

    def filter(self, words: Set[str]) -> Set[str]:
        """Filters words by using a WordleGuess.

        :param words: initial set of words to filter
        :return: filtered set of words
        """
        # Determine if any letters appear more than once (these will make exceptions).
        correct, misplaced = Counter(), Counter()
        for component in self.wordle_guess:
            if component.type == WordleGuessComponentType.MISPLACED:
                misplaced[component.letter] += 1
            elif component.type == WordleGuessComponentType.CORRECT:
                correct[component.letter] += 1

        # Determine what indices are left to guess.
        remaining_indices = [
            i
            for i, component in enumerate(self.wordle_guess)
            if component.type != WordleGuessComponentType.CORRECT
        ]

        # Select the right filter (if possible) and reduce words.
        filtered_words: Set[str] = set(words)
        for i, component in enumerate(self.wordle_guess):
            if component.type == WordleGuessComponentType.CORRECT:
                chosen_filter = CorrectLetterFilterStrategy(component.letter, i)
            elif component.type == WordleGuessComponentType.MISPLACED:
                chosen_filter = MisplacedLetterFilterStrategy(component.letter, i)
            elif component.type == WordleGuessComponentType.INCORRECT:
                # This one is a bit tricky--the logic changes for multiple letters.
                if misplaced[component.letter]:
                    chosen_filter = MisplacedLetterFilterStrategy(component.letter, i)
                elif correct[component.letter]:
                    for remaining_index in remaining_indices:
                        chosen_filter = MisplacedLetterFilterStrategy(
                            component.letter, remaining_index
                        )
                        filtered_words = chosen_filter.filter(filtered_words)
                    continue
                else:
                    chosen_filter = IncorrectLetterFilterStrategy(component.letter)
            else:
                chosen_filter = MisplacedLetterFilterStrategy(component.letter, i)
            filtered_words = chosen_filter.filter(filtered_words)
        return filtered_words
