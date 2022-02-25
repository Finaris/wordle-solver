#!/usr/bin/python3

"""A CLI version of WordleSolver."""

from os import path

from wordle_solver.language.lexicon import EnglishLexicon
from wordle_solver.language.lexicon_strategies import (
    LengthFilterStrategy,
    RandomWordSelectStrategy,
    WordleGuessFilterStrategy,
)
from wordle_solver.wordle.wordle_guess import WordleGuess

# Number of attempts in a Wordle game.
TOTAL_ATTEMPTS: int = 6

# Default word length for Wordle.
WORD_LENGTH: int = 5

# Values of confirmation and negation.
CONFIRM_OPTIONS = {"y", "yes"}
DENY_OPTIONS = {"n", "no"}
TRY_AGAIN_OPTIONS = {"t"}

# Variables which will change during execution of CLI.
lexicon: EnglishLexicon
remaining_attempts: int = TOTAL_ATTEMPTS


def play() -> None:
    """Plays a game of Wordle."""
    # Make an initial guess.
    print(f"Welcome to Wordle guesser! Initial lexicon size is: {lexicon.length}")
    first_word = lexicon.sample(RandomWordSelectStrategy())
    global remaining_attempts
    remaining_attempts -= 1
    if not confirmation_prompt(first_word):
        return win(first_word)

    # Otherwise, continue searching.
    while remaining_attempts:
        remaining_attempts -= 1
        next_word = reduce_lexicon()
        if not confirmation_prompt(next_word):
            return win(next_word)
    print(f"Unable to determine correct word in time!")


def reduce_lexicon() -> str:
    """Reduces the lexicon based on the previous guess.

    Enter in format of letters followed by type, spaces between each.
    i.e. if second letter is right and first letter is out of place
    a? b$ c! d! e!
    """
    # Get a representation of the guess to help filtering.
    raw_user_text = input(f"Enter feedback on line below:")
    guess = WordleGuess.from_user_input(raw_user_text)

    # Now do filtering.
    pre_size = lexicon.length
    lexicon.filter(WordleGuessFilterStrategy(guess))
    next_word = lexicon.sample(RandomWordSelectStrategy())
    print(f"Reduced lexicon from {pre_size} to {lexicon.length}; got {next_word}")
    return next_word


def confirmation_prompt(guessed_word: str) -> bool:
    """A CLI confirmation prompt which returns the value of the confirmation."""
    print(f"Turn {TOTAL_ATTEMPTS - remaining_attempts}/{TOTAL_ATTEMPTS}")
    print(f"Guessed word is: {guessed_word}")
    value = input("Continue? [y, n, t]").lower()
    if value in CONFIRM_OPTIONS:
        return True
    elif value in DENY_OPTIONS:
        return False
    elif value in TRY_AGAIN_OPTIONS:
        lexicon.discard(guessed_word)
        next_word = select_random_word()
        return confirmation_prompt(next_word)
    raise ValueError(f"unknown input {value}")


def select_random_word() -> str:
    """Selects a random word from the lexicon."""
    next_word = lexicon.sample(RandomWordSelectStrategy())
    print(f"Chose: {next_word}!")
    return next_word


def win(correct_word: str) -> None:
    """Winning prompt."""
    print(
        f"Congratulations, won on turn {TOTAL_ATTEMPTS-remaining_attempts}"
        f"/{TOTAL_ATTEMPTS}! Winning word was: {correct_word}"
    )


def main() -> None:
    """Main loop of the CLI solver."""
    # A massive hack to get a list of all valid words.

    containing_directory = path.dirname(path.abspath(__file__))
    # save_file = path.join(containing_directory, "data/short_words.txt")
    # with open(save_file, "w") as f:
    #     f.write("\n".join(all_valid_words))
    corpus_path = path.join(containing_directory, "data/short_words.txt")
    global lexicon
    lexicon = EnglishLexicon.from_file(corpus_path)
    lexicon.filter(LengthFilterStrategy(WORD_LENGTH))
    play()


if __name__ == "__main__":
    main()
