"""Match detector: find runs of 3+ identical symbols in rows or columns."""
from __future__ import annotations

from typing import List, Set, Tuple

from falling_bricks.models.field import Field

_MIN_MATCH = 3


class MatchDetector:
    """Scans a :class:`~falling_bricks.models.field.Field` for matches.

    A *match* is a horizontal or vertical run of three or more identical,
    non-empty symbols.  All matched cell coordinates are returned as a set so
    they can be removed in one pass (overlapping H/V matches are handled
    naturally).
    """

    def find_matches(self, field: Field) -> Set[Tuple[int, int]]:
        """Return the set of ``(row, col)`` coordinates that belong to a match."""
        matched: Set[Tuple[int, int]] = set()
        matched |= self._scan_rows(field)
        matched |= self._scan_cols(field)
        return matched

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _scan_rows(self, field: Field) -> Set[Tuple[int, int]]:
        matched: Set[Tuple[int, int]] = set()
        for row in range(field.height):
            positions = [(row, col) for col in range(field.width)]
            matched |= self._find_runs(positions, field)
        return matched

    def _scan_cols(self, field: Field) -> Set[Tuple[int, int]]:
        matched: Set[Tuple[int, int]] = set()
        for col in range(field.width):
            positions = [(row, col) for row in range(field.height)]
            matched |= self._find_runs(positions, field)
        return matched

    def _find_runs(
        self, positions: List[Tuple[int, int]], field: Field
    ) -> Set[Tuple[int, int]]:
        matched: Set[Tuple[int, int]] = set()
        i = 0
        n = len(positions)
        while i < n:
            row, col = positions[i]
            symbol = field.get(row, col)
            if symbol is None:
                i += 1
                continue
            # Find end of consecutive run with same symbol
            j = i + 1
            while j < n:
                r2, c2 = positions[j]
                if field.get(r2, c2) != symbol:
                    break
                j += 1
            run_length = j - i
            if run_length >= _MIN_MATCH:
                for k in range(i, j):
                    matched.add(positions[k])
            i = j
        return matched
