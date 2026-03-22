"""Tests for Brick."""
import pytest

from falling_bricks.models.brick import Brick, Orientation


def make_h(*symbols) -> Brick:
    return Brick(Orientation.HORIZONTAL, symbols)


def make_v(*symbols) -> Brick:
    return Brick(Orientation.VERTICAL, symbols)


class TestBrickCreation:
    def test_horizontal_stores_orientation(self):
        b = make_h("^", "^", "*")
        assert b.orientation == Orientation.HORIZONTAL

    def test_vertical_stores_orientation(self):
        b = make_v("*", "@", "^")
        assert b.orientation == Orientation.VERTICAL

    def test_symbols_stored_as_immutable_tuple(self):
        # Accepts a list but stores it as a tuple (immutable value object).
        b = Brick(Orientation.HORIZONTAL, ["~", ".", "*"])
        assert b.symbols == ("~", ".", "*")
        assert isinstance(b.symbols, tuple)

    def test_accepts_tuple_input(self):
        b = Brick(Orientation.HORIZONTAL, ("^", "^", "*"))
        assert b.symbols == ("^", "^", "*")

    def test_accepts_generator_input(self):
        b = Brick(Orientation.HORIZONTAL, (s for s in ["@", "*", "~"]))
        assert b.symbols == ("@", "*", "~")

    def test_empty_symbols_raises(self):
        with pytest.raises(ValueError):
            Brick(Orientation.HORIZONTAL, [])

    # --- Variable-length bricks (scalability) ---

    def test_two_symbol_horizontal_brick(self):
        b = make_h("^", "*")
        assert len(b.symbols) == 2

    def test_five_symbol_horizontal_brick(self):
        b = make_h("^", "*", "@", "~", ".")
        assert len(b.symbols) == 5

    def test_one_symbol_vertical_brick(self):
        b = make_v("^")
        assert len(b.symbols) == 1

    # --- Hashability (tuple[str,...] is hashable; list is not) ---

    def test_brick_is_hashable(self):
        b = make_h("^", "^", "*")
        # Should not raise — brick can be used as a dict key or in a set.
        assert hash(b) == hash(b)

    def test_brick_usable_as_dict_key(self):
        b = make_h("^", "^", "*")
        d = {b: "value"}
        assert d[b] == "value"


class TestCellsAt:
    def test_horizontal_cells_standard(self):
        b = make_h("A", "B", "C")
        assert b.cells_at(2, 1) == [(2, 1, "A"), (2, 2, "B"), (2, 3, "C")]

    def test_vertical_cells_standard(self):
        b = make_v("A", "B", "C")
        assert b.cells_at(0, 2) == [(0, 2, "A"), (1, 2, "B"), (2, 2, "C")]

    def test_horizontal_cells_at_origin(self):
        b = make_h("x", "y", "z")
        assert b.cells_at(0, 0) == [(0, 0, "x"), (0, 1, "y"), (0, 2, "z")]

    def test_horizontal_two_symbols(self):
        b = make_h("A", "B")
        assert b.cells_at(0, 0) == [(0, 0, "A"), (0, 1, "B")]

    def test_horizontal_five_symbols(self):
        b = make_h("A", "B", "C", "D", "E")
        cells = b.cells_at(1, 0)
        assert len(cells) == 5
        assert cells[-1] == (1, 4, "E")

    def test_vertical_two_symbols(self):
        b = make_v("A", "B")
        assert b.cells_at(3, 2) == [(3, 2, "A"), (4, 2, "B")]

    def test_vertical_five_symbols(self):
        b = make_v("A", "B", "C", "D", "E")
        cells = b.cells_at(0, 1)
        assert len(cells) == 5
        assert cells[-1] == (4, 1, "E")


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

    def test_horizontal_two_symbols_centered(self):
        b = make_h("^", "*")
        # (5 - 2) // 2 == 1
        assert b.start_position(5) == (0, 1)

    def test_horizontal_five_symbols_centered(self):
        b = make_h("^", "*", "@", "~", ".")
        # (7 - 5) // 2 == 1
        assert b.start_position(7) == (0, 1)

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
    def test_horizontal_standard_footprint(self):
        b = make_h("a", "b", "c")
        assert b.footprint_width == 3
        assert b.footprint_height == 1

    def test_vertical_standard_footprint(self):
        b = make_v("a", "b", "c")
        assert b.footprint_width == 1
        assert b.footprint_height == 3

    def test_horizontal_two_symbol_footprint(self):
        b = make_h("a", "b")
        assert b.footprint_width == 2
        assert b.footprint_height == 1

    def test_vertical_five_symbol_footprint(self):
        b = make_v("a", "b", "c", "d", "e")
        assert b.footprint_width == 1
        assert b.footprint_height == 5


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

    def test_equal_bricks_same_hash(self):
        a = make_h("^", "*", "@")
        b = make_h("^", "*", "@")
        assert hash(a) == hash(b)
