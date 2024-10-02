import math
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from enums.Animal import Animal
from models.Piece import Piece
from views.Board import Board
from views.MenuBar import Menubar
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor

class PlayerInterface(DogPlayerInterface):
    _tk: tk.Tk
    _canvas: tk.Canvas
    __menubar: Menubar
    _board: Board

    window_width = 1280
    window_height = 720
    middle = (window_width / 2, window_height / 2)

    node_gap = 200
    circle_radius = 40

    nodes = [
    (middle[0] - (node_gap * 2), middle[1]),  # Outer Left
    (middle[0] - node_gap, middle[1] - node_gap),  # Top Left
    (middle[0] - node_gap, middle[1]),  # Middle Left
    (middle[0] - node_gap, middle[1] + node_gap),  # Bottom Left
    (middle[0], middle[1] - node_gap),  # Top
    middle,
    (middle[0], middle[1] + node_gap),  # Bottom
    (middle[0] + node_gap, middle[1] - node_gap),  # Top Right
    (middle[0] + node_gap, middle[1]),  # Middle Right
    (middle[0] + node_gap, middle[1] + node_gap),  # Bottom Right
    (middle[0] + (node_gap * 2), middle[1]),  # Outer Right
    ]

    # Colors
    yellow = "#FFCC00"
    red = "#FF0000"


    __hare = Piece(Animal.HARE)
    __hounds = (Piece(Animal.HOUND), Piece(Animal.HOUND), Piece(Animal.HOUND))
    __dragging_item: tuple[int, tuple[int, int]] | None = None  # TODO improve type

    def __init__(self):
        super().__init__()
        self._tk = tk.Tk()
        self._tk.resizable(False, False)
        self._canvas = tk.Canvas(
            self._tk, width=self.window_width, height=self.window_height, bg="#CCCCCC"
        )

        self._board = Board(self.nodes, self._tk, self._canvas)
        
        # Init Hare position
        self.__hare.position = self.nodes[10]

        # Init Hounds positions
        self.__hounds[0].position = self.nodes[0]
        self.__hounds[1].position = self.nodes[1]
        self.__hounds[2].position = self.nodes[3]


        self._tk.title("Hare and Hounds")
        self._tk.wm_iconphoto(False, tk.PhotoImage(file="../src/images/icon.png"))

        self.__menubar = Menubar(self._tk)
        self._tk.config(menu=self.__menubar)

        self._canvas.pack()

        self._canvas.tag_bind("draggable", "<ButtonPress-1>", self.start_drag)
        self._canvas.tag_bind("draggable", "<B1-Motion>", self.drag)
        self._canvas.tag_bind("draggable", "<ButtonRelease-1>", self.end_drag)
        player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)

    def draw_pieces(self):
        self._canvas.create_oval(
            self.__hare.position[0] - self.circle_radius,
            self.__hare.position[1] - self.circle_radius,
            self.__hare.position[0] + self.circle_radius,
            self.__hare.position[1] + self.circle_radius,
            fill=self.yellow,
            outline="",
            tags=("draggable", "hare"),
        )

        for i in range(3):
            self._canvas.create_oval(
                self.__hounds[i].position[0] - self.circle_radius,
                self.__hounds[i].position[1] - self.circle_radius,
                self.__hounds[i].position[0] + self.circle_radius,
                self.__hounds[i].position[1] + self.circle_radius,
                fill=self.red,
                outline="",
                tags="draggable",
            )

    def start_drag(self, event):
        item = self._canvas.find_withtag(tk.CURRENT)

        if not item or len(item) == 0:
            return

        coord = self._canvas.coords(item[0])
        self.__dragging_item = (item[0], (coord[0], coord[1]))

    def drag(self, event):
        if not self.__dragging_item:
            return

        x = event.x
        y = event.y
        self._canvas.moveto(
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
            return self._canvas.moveto(
                self.__dragging_item[0],
                self.__dragging_item[1][0],
                self.__dragging_item[1][1],
            )

        self.__hare.position = closest_node
        self._canvas.moveto(
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
        self._board.draw_board()
        self.draw_pieces()
        self._tk.mainloop()
