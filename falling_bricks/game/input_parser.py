"""Initialization input parser."""
from __future__ import annotations

from typing import List, Tuple

from falling_bricks import config
from falling_bricks.constants import (
    ERR_EXPECTED_DIMENSIONS,
    ERR_NOT_INTEGER,
    ERR_NOT_POSITIVE,
    ERR_BRICK_FIXED_LENGTH,
    ERR_BRICK_MIN_LENGTH,
    ERR_INVALID_ORIENTATION,
    ERR_INVALID_SYMBOL,
)
from falling_bricks.models.brick import Brick, Orientation


class ParseError(ValueError):
    """Raised when the initialization string cannot be parsed."""


class InputParser:
    """Parse the initialization string into field dimensions and brick templates.

    Expected format::

        <width> <height> [brick1 brick2 …]

    Each brick token is ``<orientation>`` followed by one or more symbol chars.
    When ``config.ALLOW_DYNAMIC_BRICK_LENGTH`` is False (default), the token
    must be exactly ``config.BRICK_TOKEN_LENGTH`` characters long.

    The number of bricks is capped at ``config.MAX_BRICKS`` unless
    ``config.ALLOW_UNLIMITED_BRICKS`` is True.

    Example::

        5 8 H^^* V*@^
    """

    def parse(self, raw: str) -> Tuple[int, int, List[Brick]]:
        """Return ``(width, height, bricks)`` from *raw* input.

        :raises ParseError: if the string is malformed.
        """
        tokens = raw.strip().split()
        if len(tokens) < 2:
            raise ParseError(ERR_EXPECTED_DIMENSIONS)

        width = self._parsePositiveInt(tokens[0], "width")
        height = self._parsePositiveInt(tokens[1], "height")

        bricks: List[Brick] = []
        for token in tokens[2:]:
            if not config.ALLOW_UNLIMITED_BRICKS and len(bricks) >= config.MAX_BRICKS:
                break
            bricks.append(self._parseBrick(token))

        return width, height, bricks

    # ------------------------------------------------------------------

    @staticmethod
    def _parsePositiveInt(token: str, name: str) -> int:
        try:
            value = int(token)
        except ValueError:
            raise ParseError(ERR_NOT_INTEGER.format(name=name.capitalize(), value=token))
        if value < 1:
            raise ParseError(ERR_NOT_POSITIVE.format(name=name.capitalize(), value=value))
        return value

    @staticmethod
    def _parseBrick(token: str) -> Brick:
        if config.ALLOW_DYNAMIC_BRICK_LENGTH:
            if len(token) < 2:
                raise ParseError(ERR_BRICK_MIN_LENGTH.format(token=token, actual=len(token)))
        else:
            if len(token) != config.BRICK_TOKEN_LENGTH:
                raise ParseError(
                    ERR_BRICK_FIXED_LENGTH.format(
                        token=token,
                        expected=config.BRICK_TOKEN_LENGTH,
                        symbols=config.SYMBOLS_PER_BRICK,
                        actual=len(token),
                    )
                )

        orientationChar = token[0].upper()
        if orientationChar == "H":
            orientation = Orientation.HORIZONTAL
        elif orientationChar == "V":
            orientation = Orientation.VERTICAL
        else:
            raise ParseError(
                ERR_INVALID_ORIENTATION.format(char=token[0], token=token)
            )

        symbols = list(token[1:])
        for sym in symbols:
            if sym not in config.VALID_SYMBOLS:
                raise ParseError(
                    ERR_INVALID_SYMBOL.format(
                        sym=sym,
                        token=token,
                        allowed="".join(sorted(config.VALID_SYMBOLS)),
                    )
                )

        return Brick(orientation=orientation, symbols=symbols)
