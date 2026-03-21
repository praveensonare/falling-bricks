"""Tests for command parsing."""
from falling_bricks.game.commands import Command, parse_commands


class TestParseCommands:
    def test_empty_string(self):
        assert parse_commands("") == []

    def test_single_left(self):
        assert parse_commands("L") == [Command.LEFT]

    def test_single_right(self):
        assert parse_commands("R") == [Command.RIGHT]

    def test_single_drop(self):
        assert parse_commands("D") == [Command.DROP]

    def test_multiple_commands(self):
        assert parse_commands("LLR") == [Command.LEFT, Command.LEFT, Command.RIGHT]

    def test_lowercase_ignored(self):
        # lowercase is ignored (input is uppercased internally)
        assert parse_commands("l") == [Command.LEFT]

    def test_mixed_case(self):
        assert parse_commands("lRd") == [Command.LEFT, Command.RIGHT, Command.DROP]

    def test_invalid_chars_ignored(self):
        assert parse_commands("XLRY") == [Command.LEFT, Command.RIGHT]

    def test_spaces_ignored(self):
        assert parse_commands("L R") == [Command.LEFT, Command.RIGHT]

    def test_drop_right(self):
        assert parse_commands("DR") == [Command.DROP, Command.RIGHT]
