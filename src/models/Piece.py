from enums.Animal import Animal


class Piece:
    __animal: Animal
    __position: tuple[int, int]  # TODO use position class

    def __init__(self, animal: Animal):
        self.__animal = animal

    @property
    def animal(self):
        return self.__animal

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position: tuple[int, int]):
        self.__position = position
