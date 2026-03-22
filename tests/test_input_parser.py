"""Tests for InputParser."""
import pytest

from falling_bricks.game.input_parser import InputParser, ParseError
from falling_bricks.models.brick import Orientation


class TestValidInput:
    def setup_method(self):
        self.parser = InputParser()

    def testMinimalNoBricks(self):
        width, height, bricks = self.parser.parse("5 8")
        assert width == 5
        assert height == 8
        assert bricks == []

    def testOneHorizontalBrick(self):
        width, height, bricks = self.parser.parse("5 8 H^^*")
        assert len(bricks) == 1
        assert bricks[0].orientation == Orientation.HORIZONTAL
        assert bricks[0].symbols == ("^", "^", "*")

    def testOneVerticalBrick(self):
        _, _, bricks = self.parser.parse("5 8 V*@^")
        assert len(bricks) == 1
        assert bricks[0].orientation == Orientation.VERTICAL
        assert bricks[0].symbols == ("*", "@", "^")

    def testLowercaseOrientation(self):
        _, _, bricks = self.parser.parse("5 8 h^^*")
        assert bricks[0].orientation == Orientation.HORIZONTAL

    def testTwoBricks(self):
        _, _, bricks = self.parser.parse("5 8 H^^* V*@^")
        assert len(bricks) == 2

    def testFiveBricksAccepted(self):
        _, _, bricks = self.parser.parse("5 8 H^^* V*@^ H~.* V@~^ H***")
        assert len(bricks) == 5

    def testSixthBrickIgnored(self):
        _, _, bricks = self.parser.parse("5 8 H^^* V*@^ H~.* V@~^ H*** H...")
        assert len(bricks) == 5

    def testExtraWhitespaceIgnored(self):
        width, height, bricks = self.parser.parse("  5   8   H^^*  ")
        assert width == 5
        assert height == 8
        assert len(bricks) == 1

    def testAllValidSymbols(self):
        _, _, bricks = self.parser.parse("5 8 H~.* H*@^ H^^~")
        assert len(bricks) == 3


class TestInvalidInput:
    def setup_method(self):
        self.parser = InputParser()

    def testMissingHeight(self):
        with pytest.raises(ParseError):
            self.parser.parse("5")

    def testEmptyString(self):
        with pytest.raises(ParseError):
            self.parser.parse("")

    def testNonIntegerWidth(self):
        with pytest.raises(ParseError):
            self.parser.parse("abc 8")

    def testZeroWidth(self):
        with pytest.raises(ParseError):
            self.parser.parse("0 8")

    def testNegativeHeight(self):
        with pytest.raises(ParseError):
            self.parser.parse("5 -1")

    def testInvalidOrientation(self):
        with pytest.raises(ParseError):
            self.parser.parse("5 8 X^^*")

    def testInvalidSymbol(self):
        with pytest.raises(ParseError):
            self.parser.parse("5 8 H^^!")

    def testBrickTooShort(self):
        with pytest.raises(ParseError):
            self.parser.parse("5 8 H^*")

    def testBrickTooLong(self):
        with pytest.raises(ParseError):
            self.parser.parse("5 8 H^^**")
