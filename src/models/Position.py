from typing import TYPE_CHECKING, Optional

# Avoids circular imports
if TYPE_CHECKING:
    from models.Piece import Piece


class Position:
    _x: int
    _y: int
    _piece: Optional["Piece"]
    _adjacent_positions: list["Position"]

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
        self._adjacent_positions = []
        self._piece = None

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def adjacent_positions(self) -> list["Position"]:
        return self._adjacent_positions

    @property
    def piece(self) -> Optional["Piece"]:
        return self._piece

    @piece.setter
    def piece(self, piece: Optional["Piece"]):
        self._piece = piece

    def add_adjacent_position(self, position: "Position"):
        if position is self:
            raise ValueError("Position cannot be adjacent to itself")

        if position not in self._adjacent_positions:
            self._adjacent_positions.append(position)

        if self not in position.adjacent_positions:
            position.adjacent_positions.append(self)
