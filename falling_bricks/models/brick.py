"""Brick model: orientation, symbols, and positional helpers."""
from __future__ import annotations

from enum import Enum
from typing import Iterable, List, Tuple


class Orientation(Enum):
    HORIZONTAL = "H"
    VERTICAL = "V"


class Brick:
    """Immutable brick definition — orientation + an ordered sequence of symbols.

    Symbols are stored as a ``tuple[str, ...]`` regardless of what iterable is
    passed in, keeping the object hashable and safe to use as a dict key or in
    sets.  The length of the symbol sequence determines the brick's footprint:

    * **Horizontal** brick of *n* symbols occupies ``(row, col)`` …
      ``(row, col + n - 1)`` — i.e. *n* columns in one row.
    * **Vertical** brick of *n* symbols occupies ``(row, col)`` …
      ``(row + n - 1, col)`` — i.e. *n* rows in one column.

    Accepting an ``Iterable[str]`` in the constructor means callers can pass a
    plain ``list``, a ``tuple``, a generator, or any other sequence without
    type-checking ceremony.  Three symbols is the standard game size, but the
    class imposes no upper limit, making it ready for advanced game modes.
    """

    def __init__(self, orientation: Orientation, symbols: Iterable[str]) -> None:
        self._orientation = orientation
        # Freeze into an immutable tuple so Brick can be used as a dict key.
        self._symbols: tuple[str, ...] = tuple(symbols)
        if len(self._symbols) < 1:
            raise ValueError("A brick must have at least one symbol.")

    @property
    def orientation(self) -> Orientation:
        return self._orientation

    @property
    def symbols(self) -> tuple[str, ...]:
        """Immutable ordered sequence of block symbols."""
        return self._symbols

    # ------------------------------------------------------------------
    # Spatial helpers
    # ------------------------------------------------------------------

    def cells_at(self, row: int, col: int) -> List[Tuple[int, int, str]]:
        """Return ``[(row, col, symbol), …]`` for brick placed at *top-left* (row, col).

        Works for any brick length — two-block mini-bricks, the standard
        three-block game piece, or longer variants.
        """
        if self._orientation == Orientation.HORIZONTAL:
            return [(row, col + i, sym) for i, sym in enumerate(self._symbols)]
        # VERTICAL
        return [(row + i, col, sym) for i, sym in enumerate(self._symbols)]

    def start_position(self, field_width: int) -> Tuple[int, int]:
        """Return centered ``(row, col)`` start position for this brick.

        Centering is floor-biased (left-center for even remainders), matching
        the reference example output.
        """
        if self._orientation == Orientation.HORIZONTAL:
            col = (field_width - len(self._symbols)) // 2
        else:
            col = (field_width - 1) // 2
        return (0, col)

    @property
    def footprint_width(self) -> int:
        """Number of columns this brick occupies."""
        return len(self._symbols) if self._orientation == Orientation.HORIZONTAL else 1

    @property
    def footprint_height(self) -> int:
        """Number of rows this brick occupies."""
        return 1 if self._orientation == Orientation.HORIZONTAL else len(self._symbols)

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Brick):
            return NotImplemented
        return self._orientation == other._orientation and self._symbols == other._symbols

    def __hash__(self) -> int:
        return hash((self._orientation, self._symbols))

    def __repr__(self) -> str:
        return f"Brick({self._orientation.value}{''.join(self._symbols)})"
