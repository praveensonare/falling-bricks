"""Tests for Brick."""
import pytest

from falling_bricks.models.brick import Brick, Orientation


def makeH(*symbols) -> Brick:
    return Brick(Orientation.HORIZONTAL, symbols)


def makeV(*symbols) -> Brick:
    return Brick(Orientation.VERTICAL, symbols)


class TestBrickCreation:
    def testHorizontalStoresOrientation(self):
        b = makeH("^", "^", "*")
        assert b.orientation == Orientation.HORIZONTAL

    def testVerticalStoresOrientation(self):
        b = makeV("*", "@", "^")
        assert b.orientation == Orientation.VERTICAL

    def testSymbolsStoredAsImmutableTuple(self):
        # Accepts a list but stores it as a tuple (immutable value object).
        b = Brick(Orientation.HORIZONTAL, ["~", ".", "*"])
        assert b.symbols == ("~", ".", "*")
        assert isinstance(b.symbols, tuple)

    def testAcceptsTupleInput(self):
        b = Brick(Orientation.HORIZONTAL, ("^", "^", "*"))
        assert b.symbols == ("^", "^", "*")

    def testAcceptsGeneratorInput(self):
        b = Brick(Orientation.HORIZONTAL, (s for s in ["@", "*", "~"]))
        assert b.symbols == ("@", "*", "~")

    def testEmptySymbolsRaises(self):
        with pytest.raises(ValueError):
            Brick(Orientation.HORIZONTAL, [])

    # --- Variable-length bricks (scalability) ---

    def testTwoSymbolHorizontalBrick(self):
        b = makeH("^", "*")
        assert len(b.symbols) == 2

    def testFiveSymbolHorizontalBrick(self):
        b = makeH("^", "*", "@", "~", ".")
        assert len(b.symbols) == 5

    def testOneSymbolVerticalBrick(self):
        b = makeV("^")
        assert len(b.symbols) == 1

    # --- Hashability (tuple[str,...] is hashable; list is not) ---

    def testBrickIsHashable(self):
        b = makeH("^", "^", "*")
        assert hash(b) == hash(b)

    def testBrickUsableAsDictKey(self):
        b = makeH("^", "^", "*")
        d = {b: "value"}
        assert d[b] == "value"


class TestCellsAt:
    def testHorizontalCellsStandard(self):
        b = makeH("A", "B", "C")
        assert b.cellsAt(2, 1) == [(2, 1, "A"), (2, 2, "B"), (2, 3, "C")]

    def testVerticalCellsStandard(self):
        b = makeV("A", "B", "C")
        assert b.cellsAt(0, 2) == [(0, 2, "A"), (1, 2, "B"), (2, 2, "C")]

    def testHorizontalCellsAtOrigin(self):
        b = makeH("x", "y", "z")
        assert b.cellsAt(0, 0) == [(0, 0, "x"), (0, 1, "y"), (0, 2, "z")]

    def testHorizontalTwoSymbols(self):
        b = makeH("A", "B")
        assert b.cellsAt(0, 0) == [(0, 0, "A"), (0, 1, "B")]

    def testHorizontalFiveSymbols(self):
        b = makeH("A", "B", "C", "D", "E")
        cells = b.cellsAt(1, 0)
        assert len(cells) == 5
        assert cells[-1] == (1, 4, "E")

    def testVerticalTwoSymbols(self):
        b = makeV("A", "B")
        assert b.cellsAt(3, 2) == [(3, 2, "A"), (4, 2, "B")]

    def testVerticalFiveSymbols(self):
        b = makeV("A", "B", "C", "D", "E")
        cells = b.cellsAt(0, 1)
        assert len(cells) == 5
        assert cells[-1] == (4, 1, "E")


class TestStartPosition:
    def testHorizontalCenteredWidth5(self):
        b = makeH("^", "^", "*")
        assert b.startPosition(5) == (0, 1)

    def testHorizontalCenteredWidth6(self):
        b = makeH("^", "^", "*")
        assert b.startPosition(6) == (0, 1)

    def testHorizontalCenteredWidth3(self):
        b = makeH("^", "^", "*")
        assert b.startPosition(3) == (0, 0)

    def testHorizontalTwoSymbolsCentered(self):
        b = makeH("^", "*")
        assert b.startPosition(5) == (0, 1)

    def testHorizontalFiveSymbolsCentered(self):
        b = makeH("^", "*", "@", "~", ".")
        assert b.startPosition(7) == (0, 1)

    def testVerticalCenteredWidth5(self):
        b = makeV("*", "@", "^")
        assert b.startPosition(5) == (0, 2)

    def testVerticalCenteredWidth4(self):
        b = makeV("*", "@", "^")
        assert b.startPosition(4) == (0, 1)

    def testVerticalCenteredWidth1(self):
        b = makeV("*", "@", "^")
        assert b.startPosition(1) == (0, 0)


class TestFootprint:
    def testHorizontalStandardFootprint(self):
        b = makeH("a", "b", "c")
        assert b.footprintWidth == 3
        assert b.footprintHeight == 1

    def testVerticalStandardFootprint(self):
        b = makeV("a", "b", "c")
        assert b.footprintWidth == 1
        assert b.footprintHeight == 3

    def testHorizontalTwoSymbolFootprint(self):
        b = makeH("a", "b")
        assert b.footprintWidth == 2
        assert b.footprintHeight == 1

    def testVerticalFiveSymbolFootprint(self):
        b = makeV("a", "b", "c", "d", "e")
        assert b.footprintWidth == 1
        assert b.footprintHeight == 5


class TestEquality:
    def testEqualBricks(self):
        a = makeH("^", "*", "@")
        b = makeH("^", "*", "@")
        assert a == b

    def testUnequalOrientation(self):
        a = makeH("^", "*", "@")
        b = makeV("^", "*", "@")
        assert a != b

    def testUnequalSymbols(self):
        a = makeH("^", "*", "@")
        b = makeH("^", "^", "@")
        assert a != b

    def testEqualBricksSameHash(self):
        a = makeH("^", "*", "@")
        b = makeH("^", "*", "@")
        assert hash(a) == hash(b)
