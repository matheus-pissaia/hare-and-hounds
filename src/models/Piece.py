import typing
from enums.Animal import Animal

# Avoids circular imports
if typing.TYPE_CHECKING:
    from models.Position import Position


class Piece:
    _animal: Animal
    _position: "Position"

    def __init__(self, animal: Animal, position: "Position"):
        self._animal = animal
        self._position = None
        self.position = position

    @property
    def animal(self) -> Animal:
        return self._animal

    @property
    def position(self) -> "Position":
        return self._position

    @position.setter
    def position(self, new_position: "Position"):
        if self._position:
            self._position.piece = None  # Remove piece posicao antiga

        self._position = new_position
        self._position.piece = self  # move piece para nova posicao
