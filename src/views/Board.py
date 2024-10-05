import math
from PIL import ImageTk, Image
import tkinter as tk
from enums.Animal import Animal
from models.Position import Position
from models.Piece import Piece


class Board:
    __tk: tk.Tk
    __canvas: tk.Canvas
    __pieces: list[Piece]  # Maybe use a tuple to represent hare and hounds
    __positions: list[Position]

    __position_radius = 40
    """Radius of the position circle in px"""

    __gap_px = 200
    """Gap in pixels between positions"""

    def __init__(self, tk: tk.Tk, canvas: tk.Canvas):
        self.__tk = tk
        self.__canvas = canvas

        self.__init_positions()
        self.__init_pieces()

    @property
    def positions(self):
        return self.__positions

    def draw_board(self):
        self.__draw_edges()
        self.__draw_positions()
        self.__draw_pieces()

    def __draw_positions(self):
        for position in self.__positions:
            self.__canvas.create_oval(
                position.x - self.__position_radius,
                position.y - self.__position_radius,
                position.x + self.__position_radius,
                position.y + self.__position_radius,
                fill="black",
                outline="",
            )

    def __draw_edges(self):
        visited = []

        for position in self.__positions:
            visited.append(position)

            for adjacent_position in position.adjacent_positions:
                if adjacent_position not in visited:
                    self.__canvas.create_line(
                        position.x,
                        position.y,
                        adjacent_position.x,
                        adjacent_position.y,
                        width=8,
                        fill="white",
                    )

    def __draw_pieces(self):
        self.__hare_image = ImageTk.PhotoImage(
            Image.open("src/assets/hare.png").resize((128, 128))
        )
        self.__hound_image = ImageTk.PhotoImage(
            Image.open("src/assets/hound.png").resize((128, 128))
        )

        for piece in self.__pieces:
            image = (
                self.__hare_image if piece.animal == Animal.HARE else self.__hound_image
            )

            self.__canvas.create_image(
                piece.position.x,
                piece.position.y,
                anchor=tk.CENTER,
                image=image,
                tags="draggable",
            )

    def __init_positions(self):
        # Make sure to update TK before getting width and height
        self.__tk.update()

        window_width = self.__canvas.winfo_width()
        window_height = self.__canvas.winfo_height()

        (mid_x, mid_y) = (window_width / 2, window_height / 2)

        outer_left = Position(mid_x - (self.__gap_px * 2), mid_y)
        top_left = Position(mid_x - self.__gap_px, mid_y - self.__gap_px)
        middle_left = Position(mid_x - self.__gap_px, mid_y)
        bottom_left = Position(mid_x - self.__gap_px, mid_y + self.__gap_px)
        top = Position(mid_x, mid_y - self.__gap_px)
        middle = Position(mid_x, mid_y)
        bottom = Position(mid_x, mid_y + self.__gap_px)
        top_right = Position(mid_x + self.__gap_px, mid_y - self.__gap_px)
        middle_right = Position(mid_x + self.__gap_px, mid_y)
        bottom_right = Position(mid_x + self.__gap_px, mid_y + self.__gap_px)
        outer_right = Position(mid_x + (self.__gap_px * 2), mid_y)

        outer_left.add_adjacent_position(top_left)
        outer_left.add_adjacent_position(middle_left)
        outer_left.add_adjacent_position(bottom_left)

        top.add_adjacent_position(top_left)
        top.add_adjacent_position(top_right)

        middle_right.add_adjacent_position(top_right)
        middle_right.add_adjacent_position(bottom_right)

        bottom.add_adjacent_position(bottom_left)
        bottom.add_adjacent_position(bottom_right)

        middle_left.add_adjacent_position(top_left)
        middle_left.add_adjacent_position(bottom_left)

        middle.add_adjacent_position(top)
        middle.add_adjacent_position(bottom)
        middle.add_adjacent_position(middle_left)
        middle.add_adjacent_position(middle_right)
        middle.add_adjacent_position(top_left)
        middle.add_adjacent_position(top_right)
        middle.add_adjacent_position(bottom_left)
        middle.add_adjacent_position(bottom_right)

        outer_right.add_adjacent_position(top_right)
        outer_right.add_adjacent_position(middle_right)
        outer_right.add_adjacent_position(bottom_right)

        self.__positions = [
            outer_left,
            top_left,
            middle_left,
            bottom_left,
            top,
            middle,
            bottom,
            top_right,
            middle_right,
            bottom_right,
            outer_right,
        ]

    def __init_pieces(self):
        outer_left = self.__positions[0]
        top_left = self.__positions[1]
        bottom_left = self.__positions[3]
        outer_right = self.__positions[10]

        self.__pieces = [
            Piece(Animal.HOUND, outer_left),
            Piece(Animal.HOUND, top_left),
            Piece(Animal.HOUND, bottom_left),
            Piece(Animal.HARE, outer_right),
        ]
