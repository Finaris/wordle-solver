"""Abstraction of the English language."""

from dataclasses import dataclass, field
from string import ascii_lowercase
from typing import List, Set



# Set of all lowercase English letters.
ASCII_LOWERCASE_SET: Set[str] = set(ascii_lowercase)


@dataclass(frozen=True, eq=True)
class EnglishLexicon:
    """A searchable representation of the English language."""

    words: Set[str]

    @property
    def length(self) -> int:
        """The length of the words in the lexicon."""
        return len(self.words)

    @classmethod
    def from_file(cls, file_path: str) -> "EnglishLexicon":
        """Creates a lexicon from a file."""
        with open(file_path) as f:
            raw_words = [line.strip().lower() for line in f.readlines()]
        filtered_words = set(filter(lambda w: all(char in ASCII_LOWERCASE_SET for char in w), raw_words))
        return cls(filtered_words)

    def sample(self, word_strategy: WordStrategy) -> str:
        """Randomly selects a word """


    def filter_length(self, length: int) -> None:
        """Filters own length to provided length."""
        self.words = set(filter(lambda w: len(w) == length, self.words))

    def filter_correct_letter(self, letter: chr, position: int) -> None:
        """Filters by making sure letter in position is set."""
        self.words = set(filter(lambda w: w[position] == letter, self.words))

    def filter_remove_letter(self, letter: chr, indices_to_consider: List[int]) -> None:
        """Filters by removing the provided letter from all occurrences."""
        new_words: Set[str] = set()
        for word in self.words:
            for i in indices_to_consider:
                if word[i] == letter:
                    break
            else:
                new_words.add(word)
        self.words = new_words

    def filter_letter_in_place(self, letter: chr, position: int) -> None:
        """Filters by removing a letter in place."""
        self.words = set(filter(lambda w: w[position] != letter, self.words))

    def filter_misplaced_letter(self, letter: chr, position: int) -> None:
        """Filters by making sure letter is not in provided place."""
        self.words = set(filter(lambda w: letter in w and w[position] != letter, self.words))

    def filter_by_wordle_guess(self, wordle_guess: WordleGuess, indices_to_consider: List[int]):
        """Filters words by a provided wordle guess."""
        # If there are duplicates without the same component type, don't consider it.
        counts = Counter()
        for component in wordle_guess:
            counts[component.letter] += 1

        # Now perform the set reduction.
        for i, component in enumerate(wordle_guess):
            if component.type == WordleGuessComponentType.CORRECT:
                self.filter_correct_letter(component.letter, i)
            elif component.type == WordleGuessComponentType.INCORRECT:
                if counts[component.letter] > 1:
                    self.filter_letter_in_place(component.letter, i)
                else:
                    self.filter_remove_letter(component.letter, indices_to_consider)
            elif component.type == WordleGuessComponentType.MISPLACED:
                self.filter_misplaced_letter(component.letter, i)

    def remove_word(self, word: str) -> bool:
        """Returns true if word is in lexicon."""
        if word in self.words:
            self.words.remove(word)
            return True
        return False


def

