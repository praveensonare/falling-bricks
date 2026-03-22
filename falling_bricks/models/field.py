"""Field (game grid) model."""
from __future__ import annotations

from typing import Dict, Optional, Set, Tuple

from falling_bricks.constants import EMPTY_CELL, ERR_FIELD_DIMENSIONS


class Field:
    """Rectangular grid that holds settled block symbols.

    Cells store ``None`` when empty and a symbol string when occupied.
    The active (falling) brick is *not* stored in the field; it is rendered
    on top by the UI layer.
    """

    def __init__(self, width: int, height: int) -> None:
        if width < 1 or height < 1:
            raise ValueError(ERR_FIELD_DIMENSIONS.format(width=width, height=height))
        self._width = width
        self._height = height
        self._grid: list[list[Optional[str]]] = [
            [None] * width for _ in range(height)
        ]

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    # ------------------------------------------------------------------
    # Bounds / emptiness checks
    # ------------------------------------------------------------------

    def isInBounds(self, row: int, col: int) -> bool:
        return 0 <= row < self._height and 0 <= col < self._width

    def isEmpty(self, row: int, col: int) -> bool:
        return self._grid[row][col] is None

    # ------------------------------------------------------------------
    # Cell access
    # ------------------------------------------------------------------

    def get(self, row: int, col: int) -> Optional[str]:
        return self._grid[row][col]

    def place(self, row: int, col: int, symbol: str) -> None:
        self._grid[row][col] = symbol

    def remove(self, row: int, col: int) -> None:
        self._grid[row][col] = None

    def removeCells(self, cells: Set[Tuple[int, int]]) -> None:
        for row, col in cells:
            self.remove(row, col)

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def renderRow(self, row: int, overlay: Dict[Tuple[int, int], str] | None = None) -> str:
        """Return a formatted string for *row*, overlaying *active brick* cells."""
        if overlay is None:
            overlay = {}
        cells = []
        for col in range(self._width):
            key = (row, col)
            if key in overlay:
                cells.append(overlay[key])
            elif self._grid[row][col] is not None:
                cells.append(self._grid[row][col])
            else:
                cells.append(EMPTY_CELL)
        return "| " + " ".join(cells) + " |"

    def render(self, overlay: Dict[Tuple[int, int], str] | None = None) -> str:
        """Return full field as a newline-joined string."""
        return "\n".join(self.renderRow(r, overlay) for r in range(self._height))
