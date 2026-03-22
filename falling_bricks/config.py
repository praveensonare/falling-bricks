"""Game configuration — operator-tunable settings.

Change values here to alter game behaviour without touching game logic.
Feature flags provide opt-in extensions that keep the core engine unchanged.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Allowed symbols
# ---------------------------------------------------------------------------

#: Characters that may appear as block symbols in a brick definition.
VALID_SYMBOLS: frozenset[str] = frozenset("~.*@^")

# ---------------------------------------------------------------------------
# Brick input format
# ---------------------------------------------------------------------------

#: Total characters per brick token: 1 orientation char + N symbol chars.
#: Default 4  →  e.g. "H^^*"  (3 symbols).
#: Only enforced when ALLOW_DYNAMIC_BRICK_LENGTH is False.
BRICK_TOKEN_LENGTH: int = 4

#: Number of symbols per brick, derived from BRICK_TOKEN_LENGTH.
#: Kept explicit so the rest of the code never needs to subtract 1.
SYMBOLS_PER_BRICK: int = BRICK_TOKEN_LENGTH - 1

# ---------------------------------------------------------------------------
# Session limits
# ---------------------------------------------------------------------------

#: Maximum number of bricks accepted in a single session input.
MAX_BRICKS: int = 5

# ---------------------------------------------------------------------------
# Feature flags
# ---------------------------------------------------------------------------

#: When True, the MAX_BRICKS cap is lifted and any number of bricks may be
#: provided in one session.
ALLOW_UNLIMITED_BRICKS: bool = False

#: When True, brick tokens may have any length >= 2
#: (1 orientation char + at least 1 symbol) instead of exactly
#: BRICK_TOKEN_LENGTH.  Enables 2-block, 4-block, or N-block pieces.
ALLOW_DYNAMIC_BRICK_LENGTH: bool = False
