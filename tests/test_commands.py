"""Tests for command parsing."""
from falling_bricks.game.commands import Command, parseCommands


class TestParseCommands:
    def testEmptyString(self):
        assert parseCommands("") == []

    def testSingleLeft(self):
        assert parseCommands("L") == [Command.LEFT]

    def testSingleRight(self):
        assert parseCommands("R") == [Command.RIGHT]

    def testSingleDrop(self):
        assert parseCommands("D") == [Command.DROP]

    def testMultipleCommands(self):
        assert parseCommands("LLR") == [Command.LEFT, Command.LEFT, Command.RIGHT]

    def testLowercaseHandled(self):
        assert parseCommands("l") == [Command.LEFT]

    def testMixedCase(self):
        assert parseCommands("lRd") == [Command.LEFT, Command.RIGHT, Command.DROP]

    def testInvalidCharsIgnored(self):
        assert parseCommands("XLRY") == [Command.LEFT, Command.RIGHT]

    def testSpacesIgnored(self):
        assert parseCommands("L R") == [Command.LEFT, Command.RIGHT]

    def testDropRight(self):
        assert parseCommands("DR") == [Command.DROP, Command.RIGHT]
