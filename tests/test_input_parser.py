"""Tests for InputParser."""
import pytest

from falling_bricks.game.input_parser import InputParser, ParseError
from falling_bricks.models.brick import Orientation


class TestValidInput:
    def setup_method(self):
        self.parser = InputParser()

    def test_minimal_no_bricks(self):
        width, height, bricks = self.parser.parse("5 8")
        assert width == 5
        assert height == 8
        assert bricks == []

    def test_one_horizontal_brick(self):
        width, height, bricks = self.parser.parse("5 8 H^^*")
        assert len(bricks) == 1
        assert bricks[0].orientation == Orientation.HORIZONTAL
        assert bricks[0].symbols == ("^", "^", "*")

    def test_one_vertical_brick(self):
        _, _, bricks = self.parser.parse("5 8 V*@^")
        assert len(bricks) == 1
        assert bricks[0].orientation == Orientation.VERTICAL
        assert bricks[0].symbols == ("*", "@", "^")

    def test_lowercase_orientation(self):
        _, _, bricks = self.parser.parse("5 8 h^^*")
        assert bricks[0].orientation == Orientation.HORIZONTAL

    def test_two_bricks(self):
        _, _, bricks = self.parser.parse("5 8 H^^* V*@^")
        assert len(bricks) == 2

    def test_five_bricks_accepted(self):
        _, _, bricks = self.parser.parse("5 8 H^^* V*@^ H~.* V@~^ H***")
        assert len(bricks) == 5

    def test_sixth_brick_ignored(self):
        _, _, bricks = self.parser.parse("5 8 H^^* V*@^ H~.* V@~^ H*** H...")
        assert len(bricks) == 5

    def test_extra_whitespace_ignored(self):
        width, height, bricks = self.parser.parse("  5   8   H^^*  ")
        assert width == 5
        assert height == 8
        assert len(bricks) == 1

    def test_all_valid_symbols(self):
        _, _, bricks = self.parser.parse("5 8 H~.* H*@^ H^^~")
        assert len(bricks) == 3


class TestInvalidInput:
    def setup_method(self):
        self.parser = InputParser()

    def test_missing_height(self):
        with pytest.raises(ParseError):
            self.parser.parse("5")

    def test_empty_string(self):
        with pytest.raises(ParseError):
            self.parser.parse("")

    def test_non_integer_width(self):
        with pytest.raises(ParseError):
            self.parser.parse("abc 8")

    def test_zero_width(self):
        with pytest.raises(ParseError):
            self.parser.parse("0 8")

    def test_negative_height(self):
        with pytest.raises(ParseError):
            self.parser.parse("5 -1")

    def test_invalid_orientation(self):
        with pytest.raises(ParseError):
            self.parser.parse("5 8 X^^*")

    def test_invalid_symbol(self):
        with pytest.raises(ParseError):
            self.parser.parse("5 8 H^^!")

    def test_brick_too_short(self):
        with pytest.raises(ParseError):
            self.parser.parse("5 8 H^*")

    def test_brick_too_long(self):
        with pytest.raises(ParseError):
            self.parser.parse("5 8 H^^**")
