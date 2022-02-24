"""Abstraction of the English language."""

from dataclasses import dataclass
from string import ascii_lowercase
from typing import Set

from wordle_solver.lexicon_strategies import FilterStrategy, WordSelectStrategy

# Set of all lowercase English letters.
ASCII_LOWERCASE_SET: Set[str] = set(ascii_lowercase)


@dataclass
class EnglishLexicon:
    """A searchable representation of the English language."""

    words: Set[str]

    @property
    def length(self) -> int:
        """The length of the words in the lexicon.

        :return: the number of words in the lexicon
        """
        return len(self.words)

    @classmethod
    def from_file(cls, file_path: str) -> "EnglishLexicon":
        """Creates a lexicon from a file.

        :param file_path: path to file which contains a corpus of text
        :return: the created lexicon
        """
        with open(file_path) as f:
            raw_words = [line.strip().lower() for line in f.readlines()]
        filtered_words = set(
            filter(lambda w: all(char in ASCII_LOWERCASE_SET for char in w), raw_words)
        )
        return cls(filtered_words)

    def sample(self, word_select_strategy: WordSelectStrategy) -> str:
        """Selects a word frm the lexicon using the given strategy.

        :param word_select_strategy: a strategy for selecting a word
        :return: word chosen via strategy
        """
        return word_select_strategy.select(self.words)

    def filter(self, filter_strategy: FilterStrategy) -> None:
        """Filters the lexicon using the given strategy.

        :param filter_strategy: strategy for filtering words
        :return: None
        """
        self.words = filter_strategy.filter(set(self.words))

    def discard(self, word: str) -> bool:
        """Removes a word from the lexicon.

        :param word: word to remove
        :return: True if the word existed, False otherwise
        """
        """Returns true if word is in lexicon."""
        if word in self.words:
            self.words.discard(word)
            return True
        return False
