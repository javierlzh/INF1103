import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from get_positive_float import get_positive_float
from ui import read_number


class UserInputTests(unittest.TestCase):
    def test_price_retries_until_positive_number(self) -> None:
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]) as prompt:
            with redirect_stdout(output):
                result = get_positive_float("Price: ")
        self.assertEqual(result, 12.50)
        self.assertEqual(prompt.call_count, 3)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_price_rejects_zero_and_nonfinite_values(self) -> None:
        with patch("builtins.input", side_effect=["0", "nan", "inf", "1"]) as prompt:
            with redirect_stdout(io.StringIO()):
                self.assertEqual(get_positive_float("Price: "), 1.0)
        self.assertEqual(prompt.call_count, 4)

    def test_stock_retries_and_accepts_zero(self) -> None:
        with patch("builtins.input", side_effect=["abc", "-5", "1.5", "0"]) as prompt:
            with redirect_stdout(io.StringIO()):
                result = read_number("Stock: ", int)
        self.assertEqual(result, 0)
        self.assertIsInstance(result, int)
        self.assertEqual(prompt.call_count, 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
