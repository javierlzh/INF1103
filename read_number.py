"""Type contract for numeric-input callbacks."""

from typing import Protocol, overload


class ReadNumber(Protocol):
    """Numeric-input callback shared by the product UI factories."""

    @overload
    def __call__(self, prompt: str, number_type: type[int]) -> int: ...

    @overload
    def __call__(self, prompt: str, number_type: type[float] = float) -> float: ...
