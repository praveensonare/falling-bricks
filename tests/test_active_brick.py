"""Tests for ActiveBrick helper dataclass."""
from falling_bricks.game.engine import ActiveBrick
from falling_bricks.models.brick import Brick, Orientation


def testCellsDelegatesToTemplate():
    template = Brick(Orientation.HORIZONTAL, ("A", "B", "C"))
    ab = ActiveBrick(template=template, row=2, col=3)
    assert ab.cells() == [(2, 3, "A"), (2, 4, "B"), (2, 5, "C")]


def testOverlayReturnsDict():
    template = Brick(Orientation.VERTICAL, ("X", "Y", "Z"))
    ab = ActiveBrick(template=template, row=0, col=1)
    overlay = ab.overlay()
    assert overlay == {(0, 1): "X", (1, 1): "Y", (2, 1): "Z"}
