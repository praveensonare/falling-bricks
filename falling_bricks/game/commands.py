"""Command definitions and parsing utilities."""
from __future__ import annotations

from enum import Enum
from typing import List


class Command(Enum):
    LEFT = "L"
    RIGHT = "R"
    DROP = "D"


_CHAR_TO_COMMAND = {cmd.value: cmd for cmd in Command}


def parseCommands(raw: str) -> List[Command]:
    """Extract valid commands from *raw* input string.

    Characters that are not ``L``, ``R``, or ``D`` (case-insensitive) are
    silently ignored.
    """
    result: List[Command] = []
    for ch in raw.upper():
        cmd = _CHAR_TO_COMMAND.get(ch)
        if cmd is not None:
            result.append(cmd)
    return result
