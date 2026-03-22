"""Entry point for the Match-3 falling-bricks console game."""
from __future__ import annotations

from falling_bricks import config
from falling_bricks.constants import (
    MSG_WELCOME,
    MSG_INIT_PROMPT,
    MSG_GAME_OVER,
    MSG_GOODBYE,
    CHOICE_QUIT,
)
from falling_bricks.game.commands import parseCommands
from falling_bricks.game.engine import GameEngine, GameState
from falling_bricks.game.input_parser import InputParser, ParseError
from falling_bricks.models.field import Field
from falling_bricks.ui.console import ConsoleUI


def play(ui: ConsoleUI) -> None:
    """Run one full game session (init → game loop → game over)."""
    parser = InputParser()

    while True:
        ui.showMessage(MSG_INIT_PROMPT.format(maxBricks=config.MAX_BRICKS))

        # Keep prompting until valid initialization is provided.
        while True:
            raw = ui.getInitInput()
            try:
                width, height, bricks = parser.parse(raw)
                break
            except ParseError as exc:
                ui.showError(str(exc))

        field = Field(width, height)
        engine = GameEngine(field, bricks)

        # ---- Game loop -----------------------------------------------
        frame = 0
        while True:
            frame += 1
            ui.showFrame(frame, engine.field, engine.activeBrick)

            if engine.state == GameState.GAME_OVER:
                break

            rawCmds = ui.getCommands()
            commands = parseCommands(rawCmds)
            engine.processFrame(commands)

        # ---- Game over -----------------------------------------------
        ui.showMessage(MSG_GAME_OVER)
        choice = ui.getRestartChoice()
        if choice == CHOICE_QUIT:
            ui.showMessage(MSG_GOODBYE)
            return
        # CHOICE_RESTART → loop back to init


def main() -> None:
    ui = ConsoleUI()
    ui.showMessage(MSG_WELCOME)
    play(ui)


if __name__ == "__main__":
    main()
