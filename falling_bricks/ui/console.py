"""Console UI: display and input handling."""
from __future__ import annotations

from typing import Optional

from falling_bricks.game.engine import ActiveBrick
from falling_bricks.models.field import Field

# Public message constants — imported by callers that use showMessage().
WELCOME = "Welcome to Match-3 game!"
INIT_PROMPT = "\nPlease enter field size (width and height) and up to 5 bricks set:"
GAME_OVER_MSG = "\nGame Over."
GOODBYE = "\nThank you for playing Match-3!"
RESTART_PROMPT = "Enter S to start over or Q to quit:"

_CMD_PROMPT = (
    "Enter up to 2 commands to process before moving to the next frame "
    "(valid commands are L,R,D):"
)


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
        print(_CMD_PROMPT)
        return input()

    def getRestartChoice(self) -> str:
        """Prompt until the user enters S or Q."""
        while True:
            self.showMessage(RESTART_PROMPT)
            choice = input().strip().upper()
            if choice in ("S", "Q"):
                return choice
            self.showError("Please enter S to start over or Q to quit.")
