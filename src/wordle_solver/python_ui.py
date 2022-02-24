"""Solves Wordle through the use of some brute force searching methods."""

from collections import defaultdict
from dataclasses import dataclass, field
from tkinter import *
from typing import Any, Dict, List

########################
# Front-end components #
########################

# Count of each widget type (used to bind listeners)
widget_counts: Dict[Any, int] = defaultdict(int)


@dataclass
class Selector:
    """A selector for a letter."""

    # The widgets associated with this selector.
    state_entry: Entry
    state_button: Button

    # The numbers associated with the widgets.
    state_entry_number: int = field(init=False)
    state_button_number: int = field(init=False)

    def __post_init__(self):
        """Determines count for the contained entries and buttons."""

        #
        self.state_entry_number = widget_counts[Entry]
        widget_counts[Entry] += 1
        self.state_button_number = widget_counts[Button]
        widget_counts[Button] += 1

    def grid(self) -> None:
        """Puts self into a grid."""
        self.state_entry.grid()
        self.state_button.grid()


class Wordle(Frame):
    """A visual representation of the Wordle solver."""

    def __init__(self):
        """Creates all necessary widgets in the frame."""
        # Initializes with respect to master and sets title.
        super().__init__()
        self.master.title("Wordle Solver")

        # The rows for each solve.
        self.rows: List[Any] = []

        self._create_selector()

    def _create_selector(self) -> None:
        """Creates a selector for a letter."""
        for _ in range(WordleGame.TOTAL_ATTEMPTS):
            selector = Selector()


def main() -> None:
    """Plays game of Wordle."""
    wordle = Wordle()
    wordle.mainloop()


if __name__ == "__main__":
    main()
