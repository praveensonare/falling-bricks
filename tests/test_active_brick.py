"""Tests for ActiveBrick helper dataclass."""
from falling_bricks.game.engine import ActiveBrick
from falling_bricks.models.brick import BrickTemplate, Orientation


def test_cells_delegates_to_template():
    template = BrickTemplate(Orientation.HORIZONTAL, ("A", "B", "C"))
    ab = ActiveBrick(template=template, row=2, col=3)
    assert ab.cells() == [(2, 3, "A"), (2, 4, "B"), (2, 5, "C")]


def test_overlay_returns_dict():
    template = BrickTemplate(Orientation.VERTICAL, ("X", "Y", "Z"))
    ab = ActiveBrick(template=template, row=0, col=1)
    overlay = ab.overlay()
    assert overlay == {(0, 1): "X", (1, 1): "Y", (2, 1): "Z"}
