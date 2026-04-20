"""Immutable game constants.

Unlike config.py (operator-tunable), these values are fixed by the game rules.
Changing them requires a corresponding change to the game logic.

All user-visible strings live here so they can be reviewed, translated, or
audited in one place — no magic strings anywhere else in the codebase.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Game mechanics
# ---------------------------------------------------------------------------

#: Maximum number of commands (L, R, D) processed per frame.
MAX_COMMANDS_PER_FRAME: int = 2

#: Minimum consecutive identical symbols required to form a match.
MIN_MATCH_LENGTH: int = 3

#: Minimum number of symbols a Brick must carry.
MIN_SYMBOLS_PER_BRICK: int = 1

#: Character used to render an empty grid cell.
EMPTY_CELL: str = "."

# ---------------------------------------------------------------------------
# UI messages
# Note: {maxBricks} is substituted at runtime from config.MAX_BRICKS so
# the prompt stays accurate if the cap is changed.
# ---------------------------------------------------------------------------

MSG_WELCOME: str = "Welcome to Match-3 game!"

MSG_INIT_PROMPT: str = (
    "\nPlease enter field size (width and height) and up to {maxBricks} bricks set:"
)

#: {maxCommands} is filled from MAX_COMMANDS_PER_FRAME in the same file.
MSG_CMD_PROMPT: str = (
    f"Enter up to {MAX_COMMANDS_PER_FRAME} commands to process before moving "
    "to the next frame (valid commands are L,R,D):"
)

MSG_GAME_OVER: str = "\nGame Over."
MSG_GOODBYE: str = "\nThank you for playing Match-3!"
MSG_RESTART_PROMPT: str = "Enter S to start over or Q to quit:"

# ---------------------------------------------------------------------------
# Error message templates  (fill with str.format(**kwargs))
# ---------------------------------------------------------------------------

ERR_EXPECTED_DIMENSIONS: str = "Expected at least width and height."

ERR_NOT_INTEGER: str = "{name} must be an integer, got '{value}'."

ERR_NOT_POSITIVE: str = "{name} must be a positive integer, got {value}."

ERR_BRICK_FIXED_LENGTH: str = (
    "Brick token '{token}' must be exactly {expected} characters "
    "(orientation + {symbols} symbols), got {actual}."
)

ERR_BRICK_MIN_LENGTH: str = (
    "Brick token '{token}' must be at least 2 characters "
    "(orientation + 1 symbol), got {actual}."
)

ERR_INVALID_ORIENTATION: str = (
    "Invalid orientation '{char}' in brick '{token}'. Must be 'H' or 'V'."
)

ERR_INVALID_SYMBOL: str = (
    "Invalid symbol '{sym}' in brick '{token}'. Allowed symbols: {allowed}."
)

ERR_FIELD_DIMENSIONS: str = (
    "Field dimensions must be positive, got {width}x{height}."
)

ERR_MIN_SYMBOLS: str = "A brick must have at least {min} symbol."

ERR_TOO_MANY_BRICKS: str = (
    "Too many bricks: got {actual}, maximum allowed is {max}. "
    "Please enter at most {max} bricks."
)

ERR_INVALID_RESTART: str = "Please enter S to start over or Q to quit."

# ---------------------------------------------------------------------------
# User input choices
# ---------------------------------------------------------------------------

CHOICE_RESTART: str = "S"
CHOICE_QUIT: str = "Q"
