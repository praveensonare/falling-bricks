"""Brick model: orientation, symbols, and positional helpers."""
from __future__ import annotations

from enum import Enum
from typing import List, Tuple


class Orientation(Enum):
    HORIZONTAL = "H"
    VERTICAL = "V"


class BrickTemplate:
    """Immutable brick definition — orientation + three symbols.

    A BrickTemplate has no position; use :meth:`cells_at` to project it onto
    a grid coordinate.
    """

    def __init__(self, orientation: Orientation, symbols: Tuple[str, str, str]) -> None:
        if len(symbols) != 3:
            raise ValueError("A brick must have exactly 3 symbols.")
        self._orientation = orientation
        self._symbols: Tuple[str, str, str] = tuple(symbols)  # type: ignore[assignment]

    @property
    def orientation(self) -> Orientation:
        return self._orientation

    @property
    def symbols(self) -> Tuple[str, str, str]:
        return self._symbols

    # ------------------------------------------------------------------
    # Spatial helpers
    # ------------------------------------------------------------------

    def cells_at(self, row: int, col: int) -> List[Tuple[int, int, str]]:
        """Return ``[(row, col, symbol), …]`` for brick placed at *top-left* (row, col)."""
        if self._orientation == Orientation.HORIZONTAL:
            return [(row, col + i, self._symbols[i]) for i in range(3)]
        # VERTICAL
        return [(row + i, col, self._symbols[i]) for i in range(3)]

    def start_position(self, field_width: int) -> Tuple[int, int]:
        """Return centered (row, col) start position for this brick."""
        if self._orientation == Orientation.HORIZONTAL:
            col = (field_width - 3) // 2
        else:
            col = (field_width - 1) // 2
        return (0, col)

    @property
    def footprint_width(self) -> int:
        return 3 if self._orientation == Orientation.HORIZONTAL else 1

    @property
    def footprint_height(self) -> int:
        return 1 if self._orientation == Orientation.HORIZONTAL else 3

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BrickTemplate):
            return NotImplemented
        return self._orientation == other._orientation and self._symbols == other._symbols

    def __repr__(self) -> str:
        return f"BrickTemplate({self._orientation.value}{''.join(self._symbols)})"
