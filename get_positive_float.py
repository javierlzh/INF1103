from math import isfinite

def get_positive_float(prompt: str) -> float:
    """Prompt the user for a positive float value."""
    while True:
        try:
            value = float(input(prompt))
            if not isfinite(value) or value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError as e:
            print("Please enter a valid number, e.g. 12.50")