"""Representation of a guess in Wordle."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class WordleGuessComponentType(Enum):
    """A type of guess component."""

    CORRECT = "$"
    INCORRECT = "!"
    MISPLACED = "?"


@dataclass(frozen=True, eq=True)
class WordleGuessComponent:
    """Represents a single letter in a guess."""

    letter: str
    type: WordleGuessComponentType

    @classmethod
    def parse(cls, raw_text: str) -> "WordleGuessComponent":
        """Parses a guess component from text."""
        assert len(raw_text) == 2, f"expected only type and letter in {raw_text}"
        return cls(raw_text[0], WordleGuessComponentType(raw_text[1]))


@dataclass
class WordleGuess:
    """Encapsulates information surrounding a Wordle guess."""

    components: List[WordleGuessComponent] = field(default_factory=list)

    @classmethod
    def from_user_input(cls, user_input: str) -> "WordleGuess":
        """Determines a guess from the user input."""
        return cls(
            [
                WordleGuessComponent.parse(raw_component)
                for raw_component in user_input.split()
            ]
        )

    def __iter__(self):
        for component in self.components:
            yield component
