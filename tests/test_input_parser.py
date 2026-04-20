"""Tests for InputParser."""
import pytest

import falling_bricks.config as cfg
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

    def testSixthBrickRaisesError(self):
        with pytest.raises(ParseError, match="Too many bricks"):
            self.parser.parse("5 8 H^^* V*@^ H~.* V@~^ H*** H...")

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

    def testBrickTooShort(self, monkeypatch):
        monkeypatch.setattr(cfg, "ALLOW_DYNAMIC_BRICK_LENGTH", False)
        monkeypatch.setattr(cfg, "BRICK_TOKEN_LENGTH", 4)
        with pytest.raises(ParseError):
            self.parser.parse("5 8 H^*")

    def testBrickTooLong(self, monkeypatch):
        monkeypatch.setattr(cfg, "ALLOW_DYNAMIC_BRICK_LENGTH", False)
        monkeypatch.setattr(cfg, "BRICK_TOKEN_LENGTH", 4)
        with pytest.raises(ParseError):
            self.parser.parse("5 8 H^^**")


class TestFeatureFlags:
    """Tests for config feature flags — use monkeypatch to toggle safely."""

    def setup_method(self):
        self.parser = InputParser()

    # --- ALLOW_UNLIMITED_BRICKS ---

    def testExceedingMaxBricksRaisesError(self, monkeypatch):
        monkeypatch.setattr(cfg, "ALLOW_UNLIMITED_BRICKS", False)
        monkeypatch.setattr(cfg, "MAX_BRICKS", 5)
        with pytest.raises(ParseError, match="Too many bricks"):
            self.parser.parse("5 8 H^^* V*@^ H~.* V@~^ H*** H... V~~~")

    def testExactlyMaxBricksAccepted(self, monkeypatch):
        monkeypatch.setattr(cfg, "ALLOW_UNLIMITED_BRICKS", False)
        monkeypatch.setattr(cfg, "MAX_BRICKS", 5)
        _, _, bricks = self.parser.parse("5 8 H^^* V*@^ H~.* V@~^ H***")
        assert len(bricks) == 5

    def testAllowUnlimitedBricksIgnoresCap(self, monkeypatch):
        monkeypatch.setattr(cfg, "ALLOW_UNLIMITED_BRICKS", True)
        monkeypatch.setattr(cfg, "MAX_BRICKS", 5)
        _, _, bricks = self.parser.parse("5 8 H^^* V*@^ H~.* V@~^ H*** H... V~~~")
        assert len(bricks) == 7

    def testCustomCapRaisesErrorWhenExceeded(self, monkeypatch):
        monkeypatch.setattr(cfg, "ALLOW_UNLIMITED_BRICKS", False)
        monkeypatch.setattr(cfg, "MAX_BRICKS", 3)
        with pytest.raises(ParseError, match="Too many bricks"):
            self.parser.parse("5 8 H^^* V*@^ H~.* V@~^")

    def testCustomCapAcceptsExactlyMax(self, monkeypatch):
        monkeypatch.setattr(cfg, "ALLOW_UNLIMITED_BRICKS", False)
        monkeypatch.setattr(cfg, "MAX_BRICKS", 3)
        _, _, bricks = self.parser.parse("5 8 H^^* V*@^ H~.*")
        assert len(bricks) == 3

    # --- ALLOW_DYNAMIC_BRICK_LENGTH ---

    def testDefaultRejectsNonStandardLength(self, monkeypatch):
        monkeypatch.setattr(cfg, "ALLOW_DYNAMIC_BRICK_LENGTH", False)
        monkeypatch.setattr(cfg, "BRICK_TOKEN_LENGTH", 4)
        monkeypatch.setattr(cfg, "SYMBOLS_PER_BRICK", 3)
        with pytest.raises(ParseError):
            self.parser.parse("5 8 H^^")    # 3 chars, not 4

    def testDynamicLengthAcceptsTwoSymbolBrick(self, monkeypatch):
        monkeypatch.setattr(cfg, "ALLOW_DYNAMIC_BRICK_LENGTH", True)
        _, _, bricks = self.parser.parse("5 8 H^^")
        assert len(bricks) == 1
        assert bricks[0].symbols == ("^", "^")

    def testDynamicLengthAcceptsFiveSymbolBrick(self, monkeypatch):
        monkeypatch.setattr(cfg, "ALLOW_DYNAMIC_BRICK_LENGTH", True)
        _, _, bricks = self.parser.parse("5 8 H^^^^*")
        assert len(bricks) == 1
        assert len(bricks[0].symbols) == 5

    def testDynamicLengthRejectsOrientationOnly(self, monkeypatch):
        monkeypatch.setattr(cfg, "ALLOW_DYNAMIC_BRICK_LENGTH", True)
        with pytest.raises(ParseError):
            self.parser.parse("5 8 H")     # only orientation, no symbols

    def testDynamicLengthAndUnlimitedCombined(self, monkeypatch):
        monkeypatch.setattr(cfg, "ALLOW_DYNAMIC_BRICK_LENGTH", True)
        monkeypatch.setattr(cfg, "ALLOW_UNLIMITED_BRICKS", True)
        monkeypatch.setattr(cfg, "MAX_BRICKS", 5)
        _, _, bricks = self.parser.parse("5 8 H^^ V*@ H^^^^ V*@^ H~~~ H... V~~~")
        assert len(bricks) == 7
        assert bricks[0].symbols == ("^", "^")      # 2-symbol H brick
        assert bricks[2].symbols == ("^", "^", "^", "^")  # 4-symbol H brick
