"""Initialization input parser."""
from __future__ import annotations

from typing import List, Tuple

from falling_bricks.models.brick import BrickTemplate, Orientation

# Symbols permitted by the spec plus '^' which appears in the provided example.
VALID_SYMBOLS: frozenset[str] = frozenset("~.*@^")
_MAX_BRICKS = 5


class ParseError(ValueError):
    """Raised when the initialization string cannot be parsed."""


class InputParser:
    """Parse the initialization string into field dimensions and brick templates.

    Expected format::

        <width> <height> [brick1 brick2 … brick5]

    Each brick is ``<orientation><s1><s2><s3>`` where orientation is ``H`` or
    ``V`` (case-insensitive) and each symbol is one of ``~``, ``.``, ``*``,
    ``@``, ``^``.

    Example::

        5 8 H^^* V*@^
    """

    def parse(self, raw: str) -> Tuple[int, int, List[BrickTemplate]]:
        """Return ``(width, height, bricks)`` from *raw* input.

        :raises ParseError: if the string is malformed.
        """
        tokens = raw.strip().split()
        if len(tokens) < 2:
            raise ParseError("Expected at least width and height.")

        width = self._parse_positive_int(tokens[0], "width")
        height = self._parse_positive_int(tokens[1], "height")

        bricks: List[BrickTemplate] = []
        for token in tokens[2:]:
            if len(bricks) >= _MAX_BRICKS:
                break
            bricks.append(self._parse_brick(token))

        return width, height, bricks

    # ------------------------------------------------------------------

    @staticmethod
    def _parse_positive_int(token: str, name: str) -> int:
        try:
            value = int(token)
        except ValueError:
            raise ParseError(f"{name.capitalize()} must be an integer, got '{token}'.")
        if value < 1:
            raise ParseError(f"{name.capitalize()} must be a positive integer, got {value}.")
        return value

    @staticmethod
    def _parse_brick(token: str) -> BrickTemplate:
        if len(token) != 4:
            raise ParseError(
                f"Brick token '{token}' must be exactly 4 characters "
                f"(orientation + 3 symbols), got {len(token)}."
            )
        orientation_char = token[0].upper()
        if orientation_char == "H":
            orientation = Orientation.HORIZONTAL
        elif orientation_char == "V":
            orientation = Orientation.VERTICAL
        else:
            raise ParseError(
                f"Invalid orientation '{token[0]}' in brick '{token}'. "
                "Must be 'H' or 'V'."
            )
        symbols = tuple(token[1:])
        for sym in symbols:
            if sym not in VALID_SYMBOLS:
                raise ParseError(
                    f"Invalid symbol '{sym}' in brick '{token}'. "
                    f"Allowed symbols: {''.join(sorted(VALID_SYMBOLS))}"
                )
        return BrickTemplate(orientation=orientation, symbols=symbols)  # type: ignore[arg-type]
