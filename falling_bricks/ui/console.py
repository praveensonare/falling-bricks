"""Console UI: display and input handling."""
from __future__ import annotations

from typing import Optional

from falling_bricks.game.engine import ActiveBrick, GameState
from falling_bricks.models.field import Field


_WELCOME = "Welcome to Match-3 game!"
_INIT_PROMPT = "Please enter field size (width and height) and up to 5 bricks set:"
_CMD_PROMPT = (
    "Enter up to 2 commands to process before moving to the next frame "
    "(valid commands are L,R,D):"
)
_RESTART_PROMPT = "Enter S to start over or Q to quit:"
_GAME_OVER = "Game Over."
_GOODBYE = "Thank you for playing Match-3!"


class ConsoleUI:
    """Thin wrapper around ``print`` / ``input`` for testability."""

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------

    def show_welcome(self) -> None:
        print(_WELCOME)

    def show_init_prompt(self) -> None:
        print(f"\n{_INIT_PROMPT}")

    def show_frame(
        self,
        frame: int,
        field: Field,
        active_brick: Optional[ActiveBrick],
    ) -> None:
        overlay = active_brick.overlay() if active_brick else {}
        print(f"\nFrame {frame}")
        print(field.render(overlay))

    def show_game_over(self) -> None:
        print(f"\n{_GAME_OVER}")

    def show_restart_prompt(self) -> None:
        print(_RESTART_PROMPT)

    def show_goodbye(self) -> None:
        print(f"\n{_GOODBYE}")

    def show_error(self, message: str) -> None:
        print(f"Error: {message}")

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def get_init_input(self) -> str:
        return input()

    def get_commands(self) -> str:
        print(_CMD_PROMPT)
        return input()

    def get_restart_choice(self) -> str:
        """Prompt until the user enters S or Q."""
        while True:
            self.show_restart_prompt()
            choice = input().strip().upper()
            if choice in ("S", "Q"):
                return choice
            self.show_error("Please enter S to start over or Q to quit.")
