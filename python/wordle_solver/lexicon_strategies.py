"""Strategies for working with data contained in lexicons."""

from abc import ABC, abstractmethod
import random
from typing import Set


class WordSelectStrategy(ABC):
    """A strategy for selecting words from a lexicon."""

    @staticmethod
    @abstractmethod
    def select(words: Set[str]) -> str:
        """Selects a word from the provided lexicon.

        :param words: a set of words
        :return: a word from the set
        """
        ...


class RandomWordSelectStrategy(WordSelectStrategy):
    """Selects a word randomly."""

    @staticmethod
    def select(words: Set[str]) -> str:
        """Randomly selects a word from the set.

        :param words: a set of words
        :return: a word from the set
        """
        return random.choice(tuple(words))
