"""Entry point for the Match-3 falling-bricks console game."""
from __future__ import annotations

from falling_bricks.game.commands import parseCommands
from falling_bricks.game.engine import GameEngine, GameState
from falling_bricks.game.input_parser import InputParser, ParseError
from falling_bricks.models.field import Field
from falling_bricks.ui.console import ConsoleUI, WELCOME, INIT_PROMPT, GAME_OVER_MSG, GOODBYE


def play(ui: ConsoleUI) -> None:
    """Run one full game session (init → game loop → game over)."""
    parser = InputParser()

    while True:
        ui.showMessage(INIT_PROMPT)

        # Keep prompting until valid initialization is provided.
        while True:
            raw = ui.getInitInput()
            try:
                width, height, brickTemplates = parser.parse(raw)
                break
            except ParseError as exc:
                ui.showError(str(exc))

        field = Field(width, height)
        engine = GameEngine(field, brickTemplates)

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

            # If settling this frame caused a game-over, show the cleared
            # field as the next (final) frame before breaking.
            if engine.state == GameState.GAME_OVER:
                frame += 1
                ui.showFrame(frame, engine.field, engine.activeBrick)
                break

        # ---- Game over -----------------------------------------------
        ui.showMessage(GAME_OVER_MSG)
        choice = ui.getRestartChoice()
        if choice == "Q":
            ui.showMessage(GOODBYE)
            return
        # "S" → restart from the top of the outer while loop


def main() -> None:
    ui = ConsoleUI()
    ui.showMessage(WELCOME)
    play(ui)


if __name__ == "__main__":
    main()
