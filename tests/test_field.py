"""Tests for Field."""
import pytest

from falling_bricks.models.field import Field, EMPTY_CELL


class TestFieldCreation:
    def test_valid_dimensions(self):
        f = Field(5, 8)
        assert f.width == 5
        assert f.height == 8

    def test_invalid_width_raises(self):
        with pytest.raises(ValueError):
            Field(0, 5)

    def test_invalid_height_raises(self):
        with pytest.raises(ValueError):
            Field(5, 0)

    def test_all_cells_empty_on_creation(self):
        f = Field(3, 3)
        for row in range(3):
            for col in range(3):
                assert f.is_empty(row, col)


class TestBoundsCheck:
    def test_in_bounds(self):
        f = Field(5, 8)
        assert f.is_in_bounds(0, 0)
        assert f.is_in_bounds(7, 4)

    def test_out_of_bounds_row(self):
        f = Field(5, 8)
        assert not f.is_in_bounds(-1, 0)
        assert not f.is_in_bounds(8, 0)

    def test_out_of_bounds_col(self):
        f = Field(5, 8)
        assert not f.is_in_bounds(0, -1)
        assert not f.is_in_bounds(0, 5)


class TestPlaceAndRemove:
    def test_place_symbol(self):
        f = Field(5, 5)
        f.place(2, 3, "^")
        assert f.get(2, 3) == "^"
        assert not f.is_empty(2, 3)

    def test_remove_symbol(self):
        f = Field(5, 5)
        f.place(2, 3, "^")
        f.remove(2, 3)
        assert f.is_empty(2, 3)

    def test_remove_cells_set(self):
        f = Field(5, 5)
        f.place(0, 0, "A")
        f.place(0, 1, "B")
        f.remove_cells({(0, 0), (0, 1)})
        assert f.is_empty(0, 0)
        assert f.is_empty(0, 1)


class TestRenderRow:
    def test_empty_row(self):
        f = Field(5, 3)
        assert f.render_row(0) == "| . . . . . |"

    def test_row_with_symbol(self):
        f = Field(5, 3)
        f.place(0, 2, "^")
        assert f.render_row(0) == "| . . ^ . . |"

    def test_overlay_takes_priority_over_empty(self):
        f = Field(5, 3)
        overlay = {(0, 1): "X", (0, 3): "Y"}
        assert f.render_row(0, overlay) == "| . X . Y . |"

    def test_overlay_takes_priority_over_settled(self):
        f = Field(5, 3)
        f.place(0, 1, "Z")
        overlay = {(0, 1): "X"}
        assert f.render_row(0, overlay) == "| . X . . . |"


class TestRender:
    def test_full_render(self):
        f = Field(3, 2)
        f.place(0, 1, "A")
        result = f.render()
        lines = result.splitlines()
        assert lines[0] == "| . A . |"
        assert lines[1] == "| . . . |"
