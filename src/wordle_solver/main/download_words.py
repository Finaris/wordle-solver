"""Script for downloading relevant word sources."""

# TODO: This file is not generalizable, but most of the actual logic can stay
#       the same.

import json
import logging
import re
from os import path

import requests

# Set logger for module.
logger = logging.getLogger("download_words")


def save_words(content: str, pattern: str, file_path: str) -> None:
    """Searches the content for a set of words to save in a file.

    :param content: the content to search through
    :param pattern: pattern to use for extracting words
    :param file_path: where to save resulting word list
    :return: None
    """
    # Search for the pattern, returning if nothing is found.
    search_result = re.search(pattern, content)
    if search_result is None:
        logger.warning(f"skipping pattern {pattern} (not found)")
        return

    # Extract the relevant words into a Python list.
    match = search_result.group()
    json_words = match[match.index("[") :]
    all_valid_words = json.loads(json_words)

    # Save the words to the provided path.
    with open(file_path, "w") as f:
        f.write("\n".join(all_valid_words))


def main() -> None:
    """Makes a request and parses underlying JSON to produce word lists."""
    # Get the content to search through.
    response = requests.get("https://www.powerlanguage.co.uk/wordle/main.e65ce0a5.js")
    content = response.content.decode()

    # Save short and long words from this file.
    containing_directory = path.dirname(path.abspath(__file__))
    short_words_path = path.join(containing_directory, "../data/short_words.txt")
    save_words(content, r"var La=\[([a-z,\"]*)]", short_words_path)
    long_words_path = path.join(containing_directory, "../data/long_words.txt")
    save_words(content, r"Ta=\[([a-z,\"]*)]", long_words_path)


if __name__ == "__main__":
    main()
