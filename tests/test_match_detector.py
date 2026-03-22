"""Tests for MatchDetector."""
import pytest

from falling_bricks.game.match_detector import MatchDetector
from falling_bricks.models.field import Field


def makeField(rows: list[str]) -> Field:
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
    def testEmptyField(self):
        f = Field(5, 5)
        d = MatchDetector()
        assert d.findMatches(f) == set()

    def testTwoInARowNoMatch(self):
        f = makeField(["^^."])
        d = MatchDetector()
        assert d.findMatches(f) == set()

    def testTwoInColNoMatch(self):
        f = makeField(["^", "^", "."])
        d = MatchDetector()
        assert d.findMatches(f) == set()


class TestHorizontalMatches:
    def testExactlyThree(self):
        f = makeField(["^^^"])
        d = MatchDetector()
        assert d.findMatches(f) == {(0, 0), (0, 1), (0, 2)}

    def testFourInARow(self):
        f = makeField(["^^^^"])
        d = MatchDetector()
        assert d.findMatches(f) == {(0, 0), (0, 1), (0, 2), (0, 3)}

    def testInterruptedByDifferentSymbol(self):
        f = makeField(["^^@^^"])
        d = MatchDetector()
        assert d.findMatches(f) == set()

    def testInterruptedByEmpty(self):
        f = makeField(["^^.^^"])
        d = MatchDetector()
        assert d.findMatches(f) == set()

    def testThreeAtEndOfRow(self):
        f = makeField([".^^^"])
        d = MatchDetector()
        assert d.findMatches(f) == {(0, 1), (0, 2), (0, 3)}

    def testMatchInSecondRow(self):
        f = makeField([".....", ".***."])
        d = MatchDetector()
        assert d.findMatches(f) == {(1, 1), (1, 2), (1, 3)}


class TestVerticalMatches:
    def testExactlyThree(self):
        f = makeField(["^", "^", "^"])
        d = MatchDetector()
        assert d.findMatches(f) == {(0, 0), (1, 0), (2, 0)}

    def testFourInACol(self):
        f = makeField(["^", "^", "^", "^"])
        d = MatchDetector()
        assert d.findMatches(f) == {(0, 0), (1, 0), (2, 0), (3, 0)}

    def testInterruptedByEmpty(self):
        f = makeField(["^", "^", ".", "^", "^"])
        d = MatchDetector()
        assert d.findMatches(f) == set()


class TestCombinedMatches:
    def testHorizontalAndVerticalOverlap(self):
        f = makeField(
            [
                ".^.",
                "^^^",
                ".^.",
            ]
        )
        d = MatchDetector()
        matches = d.findMatches(f)
        assert (0, 1) in matches
        assert (1, 0) in matches
        assert (1, 1) in matches
        assert (1, 2) in matches
        assert (2, 1) in matches

    def testExampleScenarioRow7(self):
        f = Field(5, 8)
        f.place(7, 1, "^")
        f.place(7, 2, "^")
        f.place(7, 3, "^")
        f.place(7, 4, "*")
        d = MatchDetector()
        matches = d.findMatches(f)
        assert {(7, 1), (7, 2), (7, 3)} <= matches
        assert (7, 4) not in matches

    def testTwoSeparateMatchesSameRow(self):
        f = makeField(["^^^.^^^"])
        d = MatchDetector()
        matches = d.findMatches(f)
        assert {(0, 0), (0, 1), (0, 2)} <= matches
        assert {(0, 4), (0, 5), (0, 6)} <= matches
        assert (0, 3) not in matches
