"""Core game engine: state machine for the falling-bricks game."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

from falling_bricks.constants import MAX_COMMANDS_PER_FRAME
from falling_bricks.models.brick import Brick
from falling_bricks.models.field import Field
from falling_bricks.game.commands import Command
from falling_bricks.game.match_detector import MatchDetector


class GameState(Enum):
    PLAYING = "playing"
    GAME_OVER = "game_over"


@dataclass
class ActiveBrick:
    """A brick placed at a specific (row, col) position."""

    brick: Brick
    row: int
    col: int

    def cells(self) -> List[Tuple[int, int, str]]:
        """Return ``[(row, col, symbol), …]`` for all blocks."""
        return self.brick.cellsAt(self.row, self.col)

    def overlay(self) -> Dict[Tuple[int, int], str]:
        """Return a mapping ``{(row, col): symbol}`` suitable for field rendering."""
        return {(r, c): s for r, c, s in self.cells()}


class GameEngine:
    """Manages game state: active brick, settled field, frame counter.

    Lifecycle
    ---------
    1. Construction spawns the first brick (frame 1).
    2. Each call to :meth:`processFrame` advances one game frame.
    3. When :attr:`state` is ``GAME_OVER`` the final field state is ready for
       display; no further frame processing is possible.

    Command processing rules (per frame)
    -------------------------------------
    * Only the first ``MAX_COMMANDS_PER_FRAME`` commands are acted upon.
    * ``L`` / ``R``: attempt to shift the brick; silently skipped when blocked
      but still count toward the command limit.
    * ``D``: instantly drop the brick to its lowest possible resting row.
    * After commands are processed, the brick *always* descends one row
      automatically.  If it cannot descend, it settles onto the field.
    """

    def __init__(self, field: Field, bricks: List[Brick]) -> None:
        self._field = field
        self.bricks = list(bricks)
        self._matchDetector = MatchDetector()
        self._nextIndex: int = 0
        self._state: GameState = GameState.PLAYING
        self._active: Optional[ActiveBrick] = None

        self._spawnNext()

    # ------------------------------------------------------------------
    # Public read-only properties
    # ------------------------------------------------------------------

    @property
    def field(self) -> Field:
        return self._field

    @property
    def activeBrick(self) -> Optional[ActiveBrick]:
        return self._active

    @property
    def state(self) -> GameState:
        return self._state

    # ------------------------------------------------------------------
    # Public mutating method
    # ------------------------------------------------------------------

    def processFrame(self, commands: List[Command]) -> None:
        """Execute *commands* and advance physics for one frame.

        If the game is already over this is a no-op.
        """
        if self._state != GameState.PLAYING or self._active is None:
            return

        cmdCount = 0
        for cmd in commands:
            if cmdCount >= MAX_COMMANDS_PER_FRAME:
                break
            cmdCount += 1
            if cmd == Command.LEFT:
                self._shift(-1)
            elif cmd == Command.RIGHT:
                self._shift(+1)
            elif cmd == Command.DROP:
                self._dropToBottom()

        self._autoDrop()

    # ------------------------------------------------------------------
    # Private movement helpers
    # ------------------------------------------------------------------

    def _shift(self, deltaCol: int) -> None:
        activeBrick = self._active
        assert activeBrick is not None
        newCol = activeBrick.col + deltaCol
        if self._isValidPosition(activeBrick.row, newCol, activeBrick.brick):
            self._active = ActiveBrick(activeBrick.brick, activeBrick.row, newCol)

    def _dropToBottom(self) -> None:
        """Move the active brick as far down as possible without settling."""
        activeBrick = self._active
        assert activeBrick is not None
        row = activeBrick.row
        while self._isValidPosition(row + 1, activeBrick.col, activeBrick.brick):
            row += 1
        self._active.row = row

    def _autoDrop(self) -> None:
        """Drop active brick one row; settle it if it cannot descend."""
        activeBrick = self._active
        assert activeBrick is not None
        if self._isValidPosition(activeBrick.row + 1, activeBrick.col, activeBrick.brick):
            self._active.row = activeBrick.row + 1
        else:
            self._settle()

    # ------------------------------------------------------------------
    # Private settle / spawn helpers
    # ------------------------------------------------------------------

    def _settle(self) -> None:
        """Place active brick on the field, detect matches, spawn next brick."""
        brick = self._active
        assert brick is not None
        placed = set()
        for row, col, symbol in brick.cells():
            self._field.place(row, col, symbol)
            placed.add((row, col))
        self._active = None

        matches = self._matchDetector.findMatches(self._field, placed)
        if matches:
            self._field.removeCells(matches)

        self._spawnNext()

    def _spawnNext(self) -> None:
        """Attempt to spawn the next brick; transition to GAME_OVER if unable."""
        if self._nextIndex >= len(self.bricks):
            self._state = GameState.GAME_OVER
            return

        brick = self.bricks[self._nextIndex]
        row, col = brick.startPosition(self._field.width)
        activeBrick = ActiveBrick(brick=brick, row=row, col=col)

        if not self._isValidPosition(row, col, activeBrick.brick):
            self._state = GameState.GAME_OVER
            return

        self._active = activeBrick
        self._nextIndex += 1

    # ------------------------------------------------------------------
    # Private validation helper
    # ------------------------------------------------------------------

    def _isValidPosition(self, row: int, col: int, brick: Brick) -> bool:
        """Return True if *brick* can be placed at (row, col) without conflict."""
        for r, c, _ in brick.cellsAt(row, col):
            if not self._field.isInBounds(r, c):
                return False
            if not self._field.isEmpty(r, c):
                return False
        return True
