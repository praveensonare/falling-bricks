"""Tests for MatchDetector."""
import pytest

from falling_bricks.game.match_detector import MatchDetector
from falling_bricks.models.field import Field


def make_field(rows: list[str]) -> Field:
    """Build a Field from a list of row strings, e.g. ['..^', '^.^']."""
    height = len(rows)
    width = len(rows[0]) if rows else 0
    f = Field(width, height)
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != ".":
                f.place(r, c, ch)
    return f


class TestNoMatches:
    def test_empty_field(self):
        f = Field(5, 5)
        d = MatchDetector()
        assert d.find_matches(f) == set()

    def test_two_in_a_row_no_match(self):
        f = make_field(["^^."])
        d = MatchDetector()
        assert d.find_matches(f) == set()

    def test_two_in_col_no_match(self):
        f = make_field(["^", "^", "."])
        d = MatchDetector()
        assert d.find_matches(f) == set()


class TestHorizontalMatches:
    def test_exactly_three(self):
        f = make_field(["^^^"])
        d = MatchDetector()
        assert d.find_matches(f) == {(0, 0), (0, 1), (0, 2)}

    def test_four_in_a_row(self):
        f = make_field(["^^^^"])
        d = MatchDetector()
        assert d.find_matches(f) == {(0, 0), (0, 1), (0, 2), (0, 3)}

    def test_interrupted_by_different_symbol(self):
        f = make_field(["^^@^^"])
        d = MatchDetector()
        assert d.find_matches(f) == set()

    def test_interrupted_by_empty(self):
        f = make_field(["^^.^^"])
        d = MatchDetector()
        assert d.find_matches(f) == set()

    def test_three_at_end_of_row(self):
        f = make_field([".^^^"])
        d = MatchDetector()
        assert d.find_matches(f) == {(0, 1), (0, 2), (0, 3)}

    def test_match_in_second_row(self):
        f = make_field([".....", ".***."])
        d = MatchDetector()
        assert d.find_matches(f) == {(1, 1), (1, 2), (1, 3)}


class TestVerticalMatches:
    def test_exactly_three(self):
        f = make_field(["^", "^", "^"])
        d = MatchDetector()
        assert d.find_matches(f) == {(0, 0), (1, 0), (2, 0)}

    def test_four_in_a_col(self):
        f = make_field(["^", "^", "^", "^"])
        d = MatchDetector()
        assert d.find_matches(f) == {(0, 0), (1, 0), (2, 0), (3, 0)}

    def test_interrupted_by_empty(self):
        f = make_field(["^", "^", ".", "^", "^"])
        d = MatchDetector()
        assert d.find_matches(f) == set()


class TestCombinedMatches:
    def test_horizontal_and_vertical_overlap(self):
        # "+" shaped overlap
        f = make_field(
            [
                ".^.",
                "^^^",
                ".^.",
            ]
        )
        d = MatchDetector()
        matches = d.find_matches(f)
        # Vertical col 1: rows 0,1,2; Horizontal row 1: cols 0,1,2
        assert (0, 1) in matches
        assert (1, 0) in matches
        assert (1, 1) in matches
        assert (1, 2) in matches
        assert (2, 1) in matches

    def test_example_scenario_row7(self):
        # Simulates bottom of example: row has ^, ^, ^, * at cols 1-4 (width 5)
        f = Field(5, 8)
        f.place(7, 1, "^")
        f.place(7, 2, "^")
        f.place(7, 3, "^")
        f.place(7, 4, "*")
        d = MatchDetector()
        matches = d.find_matches(f)
        assert {(7, 1), (7, 2), (7, 3)} <= matches
        assert (7, 4) not in matches

    def test_two_separate_matches_same_row(self):
        # "^^^.^^^" → two independent matches
        f = make_field(["^^^.^^^"])
        d = MatchDetector()
        matches = d.find_matches(f)
        assert {(0, 0), (0, 1), (0, 2)} <= matches
        assert {(0, 4), (0, 5), (0, 6)} <= matches
        assert (0, 3) not in matches
