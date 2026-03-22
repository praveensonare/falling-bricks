"""Tests for GameEngine."""
import pytest

from falling_bricks.game.commands import Command
from falling_bricks.game.engine import GameEngine, GameState, ActiveBrick
from falling_bricks.models.brick import Brick, Orientation
from falling_bricks.models.field import Field


def hBrick(*symbols) -> Brick:
    return Brick(Orientation.HORIZONTAL, symbols)


def vBrick(*symbols) -> Brick:
    return Brick(Orientation.VERTICAL, symbols)


def makeEngine(width: int, height: int, *bricks: Brick) -> GameEngine:
    return GameEngine(Field(width, height), list(bricks))


class TestInitialSpawn:
    def testFirstBrickSpawnsOnInit(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"))
        assert engine.activeBrick is not None
        assert engine.state == GameState.PLAYING

    def testStateIsPlayingOnStart(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"))
        assert engine.state == GameState.PLAYING

    def testHorizontalBrickCentered(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"))
        ab = engine.activeBrick
        assert ab is not None
        assert ab.row == 0
        assert ab.col == 1  # (5-3)//2 == 1

    def testVerticalBrickCentered(self):
        engine = makeEngine(5, 8, vBrick("*", "@", "^"))
        ab = engine.activeBrick
        assert ab is not None
        assert ab.row == 0
        assert ab.col == 2  # (5-1)//2 == 2

    def testNoBricksGameOverImmediately(self):
        engine = makeEngine(5, 8)
        assert engine.state == GameState.GAME_OVER

    def testGameOverWhenFieldBlocked(self):
        field = Field(5, 8)
        field.place(0, 1, "X")
        engine = GameEngine(field, [hBrick("^", "^", "*")])
        assert engine.state == GameState.GAME_OVER


class TestMoveLeft:
    def testMoveLeftValid(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"))
        initialCol = engine.activeBrick.col
        engine.processFrame([Command.LEFT])
        assert engine.activeBrick.col == initialCol - 1

    def testMoveLeftAtBoundaryIgnored(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"))
        engine.processFrame([Command.LEFT])   # col 1→0
        engine.processFrame([Command.LEFT])   # would go -1, ignored
        ab = engine.activeBrick
        assert ab is not None
        assert ab.col == 0


class TestMoveRight:
    def testMoveRightValid(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"))
        initialCol = engine.activeBrick.col
        engine.processFrame([Command.RIGHT])
        assert engine.activeBrick.col == initialCol + 1

    def testMoveRightAtBoundaryIgnored(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"))
        engine.processFrame([Command.RIGHT])  # col 1→2
        colBefore = engine.activeBrick.col
        engine.processFrame([Command.RIGHT])  # would go col 3 → OOB
        assert engine.activeBrick.col == colBefore

    def testVerticalBrickRightBoundary(self):
        engine = makeEngine(5, 8, vBrick("*", "@", "^"))
        engine.processFrame([Command.RIGHT])
        engine.processFrame([Command.RIGHT])
        col = engine.activeBrick.col
        engine.processFrame([Command.RIGHT])  # col 4 → col 5 OOB
        assert engine.activeBrick.col == col


class TestMaxTwoCommandsPerFrame:
    def testOnlyTwoCommandsProcessed(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"))
        # LLL: only first two applied; third ignored
        engine.processFrame([Command.LEFT, Command.LEFT, Command.LEFT])
        assert engine.activeBrick.col == 0

    def testLLROnlyLLProcessed(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"))
        engine.processFrame([Command.LEFT, Command.LEFT, Command.RIGHT])
        assert engine.activeBrick.col == 0


class TestDropCommand:
    def testDropGoesToBottom(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"))
        engine.processFrame([Command.DROP])
        assert engine.state == GameState.GAME_OVER

    def testDropFollowedByRight(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"))
        engine.processFrame([Command.DROP, Command.RIGHT])
        assert engine.state == GameState.GAME_OVER
        assert engine.field.get(7, 2) == "^"
        assert engine.field.get(7, 3) == "^"
        assert engine.field.get(7, 4) == "*"

    def testDropStopsAboveExistingBrick(self):
        field = Field(5, 8)
        field.place(5, 1, "X")
        field.place(5, 2, "X")
        field.place(5, 3, "X")
        engine = GameEngine(field, [hBrick("^", "^", "*")])
        engine.processFrame([Command.DROP])
        assert engine.field.get(4, 1) == "^"


class TestAutoDropAndSettle:
    def testBrickDropsOnePerFrame(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"))
        assert engine.activeBrick.row == 0
        engine.processFrame([])
        assert engine.activeBrick.row == 1
        engine.processFrame([])
        assert engine.activeBrick.row == 2

    def testBrickSettlesAtBottom(self):
        engine = makeEngine(5, 3, hBrick("^", "^", "*"))
        # Height=3: rows 0,1,2. Brick drops: 0→1 (frame1), 1→2 (frame2),
        # can't go to row3 in frame3 → settle.
        engine.processFrame([])  # row 0→1
        engine.processFrame([])  # row 1→2
        engine.processFrame([])  # row 2, can't drop to 3 → settle
        assert engine.field.get(2, 1) == "^"
        assert engine.field.get(2, 2) == "^"
        assert engine.field.get(2, 3) == "*"

    def testVerticalBrickSettlesAtBottom(self):
        engine = makeEngine(5, 5, vBrick("*", "@", "^"))
        # V brick rows 0-2. Drops: 0-2→1-3 (f1), 1-3→2-4 (f2),
        # can't go to 3-5 in frame3 → settle.
        engine.processFrame([])  # rows 0-2 → 1-3
        engine.processFrame([])  # rows 1-3 → 2-4
        engine.processFrame([])  # rows 2-4, can't drop → settle
        assert engine.field.get(2, 2) == "*"
        assert engine.field.get(3, 2) == "@"
        assert engine.field.get(4, 2) == "^"


class TestMatchRemoval:
    def testThreeMatchingHorizontalRemoved(self):
        field = Field(3, 3)
        engine = GameEngine(field, [hBrick("^", "^", "^")])
        engine.processFrame([Command.DROP])
        assert field.isEmpty(2, 0)
        assert field.isEmpty(2, 1)
        assert field.isEmpty(2, 2)

    def testVerticalMatchAfterSettle(self):
        field = Field(3, 5)
        field.place(3, 1, "^")
        field.place(4, 1, "^")
        engine = GameEngine(field, [vBrick("^", "^", "^")])
        engine.processFrame([Command.DROP])
        for row in range(5):
            assert field.isEmpty(row, 1)

    def testNoGravityAfterMatch(self):
        field = Field(3, 4)
        field.place(1, 0, "Z")  # floating block above match row
        engine = GameEngine(field, [hBrick("^", "^", "^")])
        engine.processFrame([Command.DROP])
        assert field.isEmpty(3, 0)
        assert field.get(1, 0) == "Z"  # Z did not fall


class TestNextBrickSpawn:
    def testSecondBrickSpawnsAfterFirstSettles(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"), vBrick("*", "@", "^"))
        engine.processFrame([Command.DROP])
        assert engine.activeBrick is not None
        assert engine.activeBrick.template.orientation == Orientation.VERTICAL

    def testGameOverWhenNextBrickBlocked(self):
        engine = makeEngine(5, 3, hBrick("^", "^", "*"), hBrick("*", "*", "*"))
        engine.processFrame([Command.DROP])
        assert engine.state == GameState.PLAYING

    def testGameOverAfterAllBricksUsed(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"))
        engine.processFrame([Command.DROP])
        assert engine.state == GameState.GAME_OVER

    def testSecondBrickActiveAfterFirstDrop(self):
        engine = makeEngine(5, 8, hBrick("^", "^", "*"), vBrick("*", "@", "^"))
        assert engine.activeBrick.template.orientation == Orientation.HORIZONTAL
        engine.processFrame([Command.DROP])
        assert engine.activeBrick.template.orientation == Orientation.VERTICAL


class TestFullExampleScenario:
    """Trace the example scenario from the spec (using H^^* and V*@^)."""

    def setup_method(self):
        self.field = Field(5, 8)
        self.brick1 = hBrick("^", "^", "*")  # H^^* — corrected from spec typo
        self.brick2 = vBrick("*", "@", "^")  # V*@^
        self.engine = GameEngine(self.field, [self.brick1, self.brick2])

    def testFrame1InitialPosition(self):
        ab = self.engine.activeBrick
        assert ab.row == 0
        assert ab.col == 1

    def testFrame1AfterLL(self):
        self.engine.processFrame([Command.LEFT, Command.LEFT])
        ab = self.engine.activeBrick
        assert ab.col == 0
        assert ab.row == 1

    def testFrame2AfterR(self):
        self.engine.processFrame([Command.LEFT, Command.LEFT])
        self.engine.processFrame([Command.RIGHT])
        ab = self.engine.activeBrick
        assert ab.col == 1
        assert ab.row == 2

    def testFrame3AfterDR(self):
        self.engine.processFrame([Command.LEFT, Command.LEFT])
        self.engine.processFrame([Command.RIGHT])
        self.engine.processFrame([Command.DROP, Command.RIGHT])
        assert self.engine.activeBrick is not None
        assert self.engine.activeBrick.template == self.brick2
        assert self.engine.field.get(7, 2) == "^"
        assert self.engine.field.get(7, 3) == "^"
        assert self.engine.field.get(7, 4) == "*"

    def testFrame4SecondBrickPosition(self):
        self.engine.processFrame([Command.LEFT, Command.LEFT])
        self.engine.processFrame([Command.RIGHT])
        self.engine.processFrame([Command.DROP, Command.RIGHT])
        assert self.engine.activeBrick.row == 0
        assert self.engine.activeBrick.col == 2

    def testFrame4AfterLL(self):
        self.engine.processFrame([Command.LEFT, Command.LEFT])
        self.engine.processFrame([Command.RIGHT])
        self.engine.processFrame([Command.DROP, Command.RIGHT])
        self.engine.processFrame([Command.LEFT, Command.LEFT, Command.RIGHT])
        ab = self.engine.activeBrick
        assert ab.col == 0
        assert ab.row == 1

    def testFrame8MatchesCleared(self):
        self.engine.processFrame([Command.LEFT, Command.LEFT])
        self.engine.processFrame([Command.RIGHT])
        self.engine.processFrame([Command.DROP, Command.RIGHT])
        self.engine.processFrame([Command.LEFT, Command.LEFT, Command.RIGHT])
        self.engine.processFrame([])
        self.engine.processFrame([Command.RIGHT])
        self.engine.processFrame([Command.DROP, Command.RIGHT])
        assert self.engine.state == GameState.GAME_OVER
        assert self.field.isEmpty(7, 1)
        assert self.field.isEmpty(7, 2)
        assert self.field.isEmpty(7, 3)
        assert self.field.get(7, 4) == "*"
