"""Match detector: find runs of identical symbols via flood expansion."""
from __future__ import annotations

from typing import List, Optional, Set, Tuple

from falling_bricks.constants import MIN_MATCH_LENGTH
from falling_bricks.models.field import Field

# Unit direction vectors for the two axes we check.
# Each tuple is (delta_row, delta_col) for one axis; expansion walks
# both +direction and -direction from the seed cell.
_AXES: List[Tuple[int, int]] = [
    (0, 1),   # horizontal  — left / right
    (1, 0),   # vertical    — up   / down
]


class MatchDetector:
    """Detects matches by flood-expanding from seed cells.

    For each seed, walks outward along each axis while the symbol matches.
    A run is recorded only when its length reaches ``MIN_MATCH_LENGTH``
    (read from config — change that constant to require longer matches).
    """

    def findMatches(
        self,
        field: Field,
        placed: Optional[Set[Tuple[int, int]]] = None,
    ) -> Set[Tuple[int, int]]:
        """Return all ``(row, col)`` coordinates that belong to a match.

        :param placed: Seed cells (e.g. the just-settled brick positions).
            When ``None``, every non-empty cell is used as a seed.
        """
        if placed is None:
            placed = {
                (r, c)
                for r in range(field.height)
                for c in range(field.width)
                if not field.isEmpty(r, c)
            }

        matched: Set[Tuple[int, int]] = set()

        for r, c in placed:
            symbol = field.get(r, c)
            if symbol is None:
                continue

            for dr, dc in _AXES:
                run = self._expandAxis(field, r, c, symbol, dr, dc)
                if len(run) >= MIN_MATCH_LENGTH:
                    matched |= run

        return matched

    # ------------------------------------------------------------------

    def _expandAxis(
        self,
        field: Field,
        row: int,
        col: int,
        symbol: str,
        dr: int,
        dc: int,
    ) -> Set[Tuple[int, int]]:
        """Walk from ``(row, col)`` in both ±(dr, dc) directions.

        Stops as soon as a cell is out-of-bounds, empty, or a different
        symbol.  Returns all collected cells including the origin.
        The run length is unbounded — ``MIN_MATCH_LENGTH`` is checked by
        the caller, so changing that constant is the only knob needed.
        """
        run: Set[Tuple[int, int]] = set()
        for direction in (+1, -1):
            r, c = row, col
            while field.isInBounds(r, c) and field.get(r, c) == symbol:
                run.add((r, c))
                r, c = r + direction * dr, c + direction * dc
        return run
