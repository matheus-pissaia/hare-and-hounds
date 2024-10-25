from tkinter import Tk, Menu


class Menubar(Menu):
    __tk: Tk
    __match_dropdown: Menu

    def __init__(self, tk: Tk, **kwargs):
        super().__init__(tk, **kwargs)
        self.__tk = tk
        self.__tk.config(menu=self)

    @property
    def match_dropdown(self):
        return self.__match_dropdown

    def build_match_dropdown(self, start_match_command: callable):
        self.__match_dropdown = Menu(self.__tk, tearoff=0)

        self.add_cascade(label="Partida", menu=self.__match_dropdown)
        self.__match_dropdown.add_command(
            label="Iniciar partida",
            command=start_match_command,
        )
