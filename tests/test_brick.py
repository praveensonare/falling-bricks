"""Tests for BrickTemplate."""
import pytest

from falling_bricks.models.brick import BrickTemplate, Orientation


def make_h(*symbols) -> BrickTemplate:
    return BrickTemplate(Orientation.HORIZONTAL, symbols)


def make_v(*symbols) -> BrickTemplate:
    return BrickTemplate(Orientation.VERTICAL, symbols)


class TestBrickTemplateCreation:
    def test_horizontal_stores_orientation(self):
        b = make_h("^", "^", "*")
        assert b.orientation == Orientation.HORIZONTAL

    def test_vertical_stores_orientation(self):
        b = make_v("*", "@", "^")
        assert b.orientation == Orientation.VERTICAL

    def test_stores_symbols(self):
        b = make_h("~", ".", "*")
        assert b.symbols == ("~", ".", "*")

    def test_wrong_symbol_count_raises(self):
        with pytest.raises(ValueError):
            BrickTemplate(Orientation.HORIZONTAL, ("a", "b"))  # type: ignore[arg-type]


class TestCellsAt:
    def test_horizontal_cells(self):
        b = make_h("A", "B", "C")
        assert b.cells_at(2, 1) == [(2, 1, "A"), (2, 2, "B"), (2, 3, "C")]

    def test_vertical_cells(self):
        b = make_v("A", "B", "C")
        assert b.cells_at(0, 2) == [(0, 2, "A"), (1, 2, "B"), (2, 2, "C")]

    def test_horizontal_cells_at_origin(self):
        b = make_h("x", "y", "z")
        assert b.cells_at(0, 0) == [(0, 0, "x"), (0, 1, "y"), (0, 2, "z")]


class TestStartPosition:
    def test_horizontal_centered_width5(self):
        b = make_h("^", "^", "*")
        assert b.start_position(5) == (0, 1)

    def test_horizontal_centered_width6(self):
        b = make_h("^", "^", "*")
        assert b.start_position(6) == (0, 1)

    def test_horizontal_centered_width3(self):
        b = make_h("^", "^", "*")
        assert b.start_position(3) == (0, 0)

    def test_vertical_centered_width5(self):
        b = make_v("*", "@", "^")
        assert b.start_position(5) == (0, 2)

    def test_vertical_centered_width4(self):
        b = make_v("*", "@", "^")
        assert b.start_position(4) == (0, 1)

    def test_vertical_centered_width1(self):
        b = make_v("*", "@", "^")
        assert b.start_position(1) == (0, 0)


class TestFootprint:
    def test_horizontal_footprint(self):
        b = make_h("a", "b", "c")
        assert b.footprint_width == 3
        assert b.footprint_height == 1

    def test_vertical_footprint(self):
        b = make_v("a", "b", "c")
        assert b.footprint_width == 1
        assert b.footprint_height == 3


class TestEquality:
    def test_equal_bricks(self):
        a = make_h("^", "*", "@")
        b = make_h("^", "*", "@")
        assert a == b

    def test_unequal_orientation(self):
        a = make_h("^", "*", "@")
        b = make_v("^", "*", "@")
        assert a != b

    def test_unequal_symbols(self):
        a = make_h("^", "*", "@")
        b = make_h("^", "^", "@")
        assert a != b
