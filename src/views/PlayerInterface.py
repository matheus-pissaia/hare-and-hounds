import math
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from views.Board import Board
from views.MenuBar import Menubar
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor


class PlayerInterface(DogPlayerInterface):
    __tk: tk.Tk
    __canvas: tk.Canvas
    __menubar: Menubar
    __board: Board

    # Colors
    yellow = "#FFCC00"
    red = "#FF0000"

    window_width = 1280
    window_height = 720
    circle_radius = 20

    __dragging_item: tuple[int, tuple[int, int]] | None = None  # TODO improve type

    def __init__(self):
        super().__init__()
        self.__tk = tk.Tk()
        self.__tk.resizable(False, False)
        self.__tk.title("Hare and Hounds")
        self.__tk.wm_iconphoto(False, tk.PhotoImage(file="../src/images/icon.png"))

        self.__menubar = Menubar(self.__tk)
        self.__tk.config(menu=self.__menubar)

        self.__canvas = tk.Canvas(
            self.__tk, width=self.window_width, height=self.window_height, bg="#CCCCCC"
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

    def start_drag(self, event):
        item = self.__canvas.find_withtag(tk.CURRENT)

        if not item or len(item) == 0:
            return

        coord = self.__canvas.coords(item[0])
        self.__dragging_item = (item[0], (coord[0], coord[1]))

    # TODO add drag events pieces
    def drag(self, event):
        if not self.__dragging_item:
            return

        x = event.x
        y = event.y
        self.__canvas.moveto(
            self.__dragging_item[0],
            x - self.circle_radius,
            y - self.circle_radius,
        )

    def end_drag(self, event):
        if not self.__dragging_item:
            return

        closest_node = self.get_closest_node(event.x, event.y)
        in_node_bounds = (
            abs(closest_node[0] - event.x) <= self.circle_radius
            and abs(closest_node[1] - event.y) <= self.circle_radius
        )

        if not in_node_bounds:
            # Snap back to original position
            return self.__canvas.moveto(
                self.__dragging_item[0],
                self.__dragging_item[1][0],
                self.__dragging_item[1][1],
            )

        self.__hare.position = closest_node
        self.__canvas.moveto(
            self.__dragging_item[0],
            closest_node[0] - self.circle_radius,
            closest_node[1] - self.circle_radius,
        )
        self.__dragging_item = None

    def get_closest_node(self, x, y):
        min_distance = float("inf")
        closest_node = None

        for node in self.nodes:
            distance = math.sqrt((x - node[0]) ** 2 + (y - node[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_node = node

        return closest_node

    def start(self):
        self.__board.draw_board()
        self.__tk.mainloop()
