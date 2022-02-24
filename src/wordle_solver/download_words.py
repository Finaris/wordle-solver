"""Script for downloading relevant word sources."""

import json
import re
from os import path

import requests


def save_words(content: str, pattern: str, file_path: str) -> None:
    """Searches the content for a set of words to save in a file.

    :param content: the content to search through
    :param pattern: pattern to use for extracting words
    :param file_path: where to save resulting word list
    :return: None
    """
    # Extract the relevant words into a Python list.
    match = re.search(pattern, content).group()
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
    short_words_path = path.join(containing_directory, "data/short_words.txt")
    save_words(content, r"var La=\[([a-z,\"]*)]", short_words_path)
    long_words_path = path.join(containing_directory, "data/long_words.txt")
    save_words(content, r"Ta=\[([a-z,\"]*)]", long_words_path)


if __name__ == "__main__":
    main()
