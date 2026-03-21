"""Entry point for the Match-3 falling-bricks console game."""
from __future__ import annotations

from falling_bricks.game.commands import parse_commands
from falling_bricks.game.engine import GameEngine, GameState
from falling_bricks.game.input_parser import InputParser, ParseError
from falling_bricks.models.field import Field
from falling_bricks.ui.console import ConsoleUI


def play(ui: ConsoleUI) -> None:
    """Run one full game session (init → game loop → game over)."""
    parser = InputParser()

    while True:
        ui.show_init_prompt()

        # Keep prompting until valid initialization is provided.
        while True:
            raw = ui.get_init_input()
            try:
                width, height, brick_templates = parser.parse(raw)
                break
            except ParseError as exc:
                ui.show_error(str(exc))

        field = Field(width, height)
        engine = GameEngine(field, brick_templates)

        # ---- Game loop -----------------------------------------------
        frame = 0
        while True:
            frame += 1
            ui.show_frame(frame, engine.field, engine.active_brick)

            if engine.state == GameState.GAME_OVER:
                break

            raw_cmds = ui.get_commands()
            commands = parse_commands(raw_cmds)
            engine.process_frame(commands)

            # If settling this frame caused a game-over, show the cleared
            # field as the next (final) frame before breaking.
            if engine.state == GameState.GAME_OVER:
                frame += 1
                ui.show_frame(frame, engine.field, engine.active_brick)
                break

        # ---- Game over -----------------------------------------------
        ui.show_game_over()
        choice = ui.get_restart_choice()
        if choice == "Q":
            ui.show_goodbye()
            return
        # "S" → restart from the top of the outer while loop


def main() -> None:
    ui = ConsoleUI()
    ui.show_welcome()
    play(ui)


if __name__ == "__main__":
    main()
