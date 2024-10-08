from typing import TYPE_CHECKING, Optional

# Avoids circular imports
if TYPE_CHECKING:
    from models.Piece import Piece


class Position:
    __x: int
    __y: int
    __piece: Optional["Piece"]
    __adjacent_positions: list["Position"]

    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y
        self.__adjacent_positions = []
        self.__piece = None

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def adjacent_positions(self) -> list["Position"]:
        return self.__adjacent_positions

    @property
    def piece(self) -> Optional["Piece"]:
        return self.__piece

    @piece.setter
    def piece(self, piece: Optional["Piece"]):
        self.__piece = piece

    def add_adjacent_position(self, position: "Position"):
        if position is self:
            raise ValueError("Position cannot be adjacent to itself")

        if position not in self.__adjacent_positions:
            self.__adjacent_positions.append(position)

        if self not in position.adjacent_positions:
            position.adjacent_positions.append(self)
