"""Tests for Field."""
import pytest

from falling_bricks.models.field import Field, EMPTY_CELL


class TestFieldCreation:
    def testValidDimensions(self):
        f = Field(5, 8)
        assert f.width == 5
        assert f.height == 8

    def testInvalidWidthRaises(self):
        with pytest.raises(ValueError):
            Field(0, 5)

    def testInvalidHeightRaises(self):
        with pytest.raises(ValueError):
            Field(5, 0)

    def testAllCellsEmptyOnCreation(self):
        f = Field(3, 3)
        for row in range(3):
            for col in range(3):
                assert f.isEmpty(row, col)


class TestBoundsCheck:
    def testInBounds(self):
        f = Field(5, 8)
        assert f.isInBounds(0, 0)
        assert f.isInBounds(7, 4)

    def testOutOfBoundsRow(self):
        f = Field(5, 8)
        assert not f.isInBounds(-1, 0)
        assert not f.isInBounds(8, 0)

    def testOutOfBoundsCol(self):
        f = Field(5, 8)
        assert not f.isInBounds(0, -1)
        assert not f.isInBounds(0, 5)


class TestPlaceAndRemove:
    def testPlaceSymbol(self):
        f = Field(5, 5)
        f.place(2, 3, "^")
        assert f.get(2, 3) == "^"
        assert not f.isEmpty(2, 3)

    def testRemoveSymbol(self):
        f = Field(5, 5)
        f.place(2, 3, "^")
        f.remove(2, 3)
        assert f.isEmpty(2, 3)

    def testRemoveCellsSet(self):
        f = Field(5, 5)
        f.place(0, 0, "A")
        f.place(0, 1, "B")
        f.removeCells({(0, 0), (0, 1)})
        assert f.isEmpty(0, 0)
        assert f.isEmpty(0, 1)


class TestRenderRow:
    def testEmptyRow(self):
        f = Field(5, 3)
        assert f.renderRow(0) == "| . . . . . |"

    def testRowWithSymbol(self):
        f = Field(5, 3)
        f.place(0, 2, "^")
        assert f.renderRow(0) == "| . . ^ . . |"

    def testOverlayTakesPriorityOverEmpty(self):
        f = Field(5, 3)
        overlay = {(0, 1): "X", (0, 3): "Y"}
        assert f.renderRow(0, overlay) == "| . X . Y . |"

    def testOverlayTakesPriorityOverSettled(self):
        f = Field(5, 3)
        f.place(0, 1, "Z")
        overlay = {(0, 1): "X"}
        assert f.renderRow(0, overlay) == "| . X . . . |"


class TestRender:
    def testFullRender(self):
        f = Field(3, 2)
        f.place(0, 1, "A")
        result = f.render()
        lines = result.splitlines()
        assert lines[0] == "| . A . |"
        assert lines[1] == "| . . . |"
