from tkinter import Tk, Menu


class Menubar(Menu):
    __tk: Tk
    __match_dropdown: Menu

    def __init__(self, tk: Tk, **kwargs):
        super().__init__(tk, **kwargs)
        self.__tk = tk
        self.__match_dropdown = self._build_match_dropdown()

    def __startMatch(self):
        pass

    def _build_match_dropdown(self):
        match = Menu(self.__tk, tearoff=0)

        self.add_cascade(label="Partida", menu=match)
        match.add_command(
            label="Iniciar partida", command=self.__startMatch, state="disabled"
        )

        return match
