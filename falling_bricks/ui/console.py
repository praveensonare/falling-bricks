"""Console UI: display and input handling."""
from __future__ import annotations

from typing import Optional

from falling_bricks import config
from falling_bricks.constants import (
    MSG_CMD_PROMPT,
    MSG_RESTART_PROMPT,
    ERR_INVALID_RESTART,
    CHOICE_RESTART,
    CHOICE_QUIT,
)
from falling_bricks.game.engine import ActiveBrick
from falling_bricks.models.field import Field


class ConsoleUI:
    """Thin wrapper around ``print`` / ``input`` for testability."""

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------

    def showMessage(self, message: str) -> None:
        """Print *message* to stdout. Used for all plain text announcements."""
        print(message)

    def showFrame(
        self,
        frame: int,
        field: Field,
        activeBrick: Optional[ActiveBrick],
    ) -> None:
        overlay = activeBrick.overlay() if activeBrick else {}
        print(f"\nFrame {frame}")
        print(field.render(overlay))

    def showError(self, message: str) -> None:
        print(f"Error: {message}")

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def getInitInput(self) -> str:
        return input()

    def getCommands(self) -> str:
        print(MSG_CMD_PROMPT)
        return input()

    def getRestartChoice(self) -> str:
        """Prompt until the user enters a valid restart choice."""
        while True:
            self.showMessage(MSG_RESTART_PROMPT)
            choice = input().strip().upper()
            if choice in (CHOICE_RESTART, CHOICE_QUIT):
                return choice
            self.showError(ERR_INVALID_RESTART)
