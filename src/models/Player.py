from enums.Animal import Animal


class Player:
    __id: str
    __name: str
    __animal: Animal

    __has_turn = False
    __is_winner = False

    def __init__(self, id: str, name: str, animal: Animal):
        self.__id = id
        self.__name = name
        self.__animal = animal

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def animal(self) -> Animal:
        return self.__animal

    @property
    def has_turn(self) -> bool:
        return self.__has_turn

    @property
    def is_winner(self) -> bool:
        return self.__is_winner

    def set_winner(self):
        self.__is_winner = True

    def toggle_turn(self):
        self.__has_turn = not self.__has_turn
