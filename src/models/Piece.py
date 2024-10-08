import typing
from enums.Animal import Animal

# Avoids circular imports
if typing.TYPE_CHECKING:
    from models.Position import Position


class Piece:
    __animal: Animal
    __position: "Position"

    def __init__(self, animal: Animal, position: "Position"):
        self.__animal = animal
        self.__position = position
        self.__position.piece = self

    @property
    def animal(self) -> Animal:
        return self.__animal

    @property
    def position(self) -> "Position":
        return self.__position

    @position.setter
    def position(self, new_position: "Position"):
        self.position.piece = None
        self.__position = new_position
        self.__position.piece = self