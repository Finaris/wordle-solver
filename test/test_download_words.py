"""Tests for downloading word lists."""

from unittest import TestCase
from unittest.mock import patch

from wordle_solver.main.download_words import logger, save_words


class TestDownloadWords(TestCase):
    """Makes sure word lists are downloaded correctly."""

    def setUp(self) -> None:
        """Ignore logger outputs."""
        logger.disabled = True

    @patch("wordle_solver.main.download_words.open")
    def test_save_words(self, mock_open):
        """Makes sure words are saved when found."""
        # Create a fake write method.
        written = False

        def write(*_):
            nonlocal written
            written = True

        mock_open.return_value.__enter__.return_value.write.side_effect = write

        # If the pattern is not found, None should be returned.
        save_words("abcdefg", r"h", "")
        self.assertFalse(written)

        # Now try when a pattern is found.
        written = False
        save_words('test=["a"]', r"test=\[([a-z,\"]*)]", "")
        self.assertTrue(written)
