import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from models.Position import Position
from views.Board import Board
from views.MenuBar import Menubar
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor


class PlayerInterface(DogPlayerInterface):
    __tk: tk.Tk
    __canvas: tk.Canvas
    __menubar: Menubar
    __board: Board
    __window_width = 1280
    __window_height = 720
    __dragging_item: tuple[int, Position] | None = None

    def __init__(self):
        super().__init__()
        self.__tk = tk.Tk()
        self.__tk.resizable(False, False)
        self.__tk.title("Hare and Hounds")
        self.__tk.wm_iconphoto(False, tk.PhotoImage(file="../src/images/icon.png"))

        self.__menubar = Menubar(self.__tk)
        self.__tk.config(menu=self.__menubar)

        self.__canvas = tk.Canvas(
            self.__tk,
            width=self.__window_width,
            height=self.__window_height,
            bg="#CCCCCC",
        )

        self.__canvas.pack()

        self.__canvas.tag_bind("draggable", "<ButtonPress-1>", self.start_drag)
        self.__canvas.tag_bind("draggable", "<B1-Motion>", self.drag)
        self.__canvas.tag_bind("draggable", "<ButtonRelease-1>", self.end_drag)

        self.__board = Board(self.__tk, self.__canvas)

        player_name = simpledialog.askstring(
            title="Player identification", prompt="Qual o seu nome?"
        )
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)

    def start_drag(self, event: tk.Event):
        item = self.__canvas.find_withtag(tk.CURRENT)

        if not item or len(item) == 0:
            return

        coord = self.__canvas.coords(item[0])
        from_position = self.__board.get_position(coord[0], coord[1])

        if not from_position:
            raise Exception("Piece was intialized with an invalid position")

        self.__dragging_item = (item[0], from_position)

    def drag(self, event: tk.Event):
        if self.__dragging_item:
            self.update_piece_screen_position(event.x, event.y)

    def end_drag(self, event: tk.Event):
        if not self.__dragging_item:
            return

        from_position = self.__dragging_item[1]
        to_position = self.__board.get_position(event.x, event.y)
        valid_move = self.__board.is_valid_move(from_position, to_position)

        if not to_position or not valid_move:
            # Return piece back to initial position
            return self.update_piece_screen_position(from_position.x, from_position.y)

        self.__board.move_piece(from_position, to_position)
        self.update_piece_screen_position(to_position.x, to_position.y)

        self.__dragging_item = None

    def update_piece_screen_position(self, x: int, y: int):
        self.__canvas.moveto(
            self.__dragging_item[0],
            x - self.__board.image_radius,
            y - self.__board.image_radius,
        )

    def start(self):
        self.__board.draw_board()
        self.__tk.mainloop()
