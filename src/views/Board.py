import math
from PIL import ImageTk, Image
import tkinter as tk
from enums.Animal import Animal
from models.Position import Position
from models.Piece import Piece


class Board:
    __positions: list[Position]

    #Atributos da implementacao visual
    __tk: tk.Tk
    __canvas: tk.Canvas
    __position_radius = 40
    """Radius of the position circle in px"""

    __gap_px = 200
    """Gap in pixels between positions"""

    __image_radius = 64
    __image_size = __image_radius * 2
    """Size of the image in px"""

    __hare_image: ImageTk.PhotoImage
    __hound_image: ImageTk.PhotoImage

    def __init__(self, tk_root: tk.Tk, canvas: tk.Canvas):
        self.__tk = tk_root
        self.__canvas = canvas

        self.__init_images()
        self.__init_positions()
        self.__init_pieces()

    @property
    def positions(self):
        return self.__positions

    @property
    def image_radius(self):
        return self.__image_radius

    def draw_board(self):
        self.__draw_edges()
        self.__draw_positions()
        self.__draw_pieces()

    def __init_images(self):
        """Initialize images once to avoid reloading every time."""
        self.__hare_image = ImageTk.PhotoImage(
            Image.open("src/images/hare.png").resize(
                (self.__image_size, self.__image_size)
            )
        )
        self.__hound_image = ImageTk.PhotoImage(
            Image.open("src/images/hound.png").resize(
                (self.__image_size, self.__image_size)
            )
        )

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
        visited = set()

        for position in self.__positions:
            visited.add(position)
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
        for position in self.__positions:
            piece = position.piece
            if piece:
                image = (
                    self.__hare_image
                    if piece.animal == Animal.HARE
                    else self.__hound_image
                )
                self.__canvas.create_image(
                    position.x,
                    position.y,
                    anchor=tk.CENTER,
                    image=image,
                    tags="draggable",
                )

    def __init_positions(self):
        # Make sure to update TK before getting width and height
        self.__tk.update()

        window_width = self.__canvas.winfo_width()
        window_height = self.__canvas.winfo_height()

        mid_x, mid_y = window_width / 2, window_height / 2

        positions_dict = {}

        # posicoes tabuleiro
        positions_dict['outer_left'] = Position(mid_x - (self.__gap_px * 2), mid_y)
        positions_dict['top_left'] = Position(mid_x - self.__gap_px, mid_y - self.__gap_px)
        positions_dict['middle_left'] = Position(mid_x - self.__gap_px, mid_y)
        positions_dict['bottom_left'] = Position(mid_x - self.__gap_px, mid_y + self.__gap_px)
        positions_dict['top'] = Position(mid_x, mid_y - self.__gap_px)
        positions_dict['middle'] = Position(mid_x, mid_y)
        positions_dict['bottom'] = Position(mid_x, mid_y + self.__gap_px)
        positions_dict['top_right'] = Position(mid_x + self.__gap_px, mid_y - self.__gap_px)
        positions_dict['middle_right'] = Position(mid_x + self.__gap_px, mid_y)
        positions_dict['bottom_right'] = Position(mid_x + self.__gap_px, mid_y + self.__gap_px)
        positions_dict['outer_right'] = Position(mid_x + (self.__gap_px * 2), mid_y)

        # posicoes adjacentes
        positions_dict['outer_left'].add_adjacent_position(positions_dict['top_left'])
        positions_dict['outer_left'].add_adjacent_position(positions_dict['middle_left'])
        positions_dict['outer_left'].add_adjacent_position(positions_dict['bottom_left'])

        positions_dict['top'].add_adjacent_position(positions_dict['top_left'])
        positions_dict['top'].add_adjacent_position(positions_dict['top_right'])

        positions_dict['middle_right'].add_adjacent_position(positions_dict['top_right'])
        positions_dict['middle_right'].add_adjacent_position(positions_dict['bottom_right'])

        positions_dict['bottom'].add_adjacent_position(positions_dict['bottom_left'])
        positions_dict['bottom'].add_adjacent_position(positions_dict['bottom_right'])

        positions_dict['middle_left'].add_adjacent_position(positions_dict['top_left'])
        positions_dict['middle_left'].add_adjacent_position(positions_dict['bottom_left'])

        positions_dict['middle'].add_adjacent_position(positions_dict['top'])
        positions_dict['middle'].add_adjacent_position(positions_dict['bottom'])
        positions_dict['middle'].add_adjacent_position(positions_dict['middle_left'])
        positions_dict['middle'].add_adjacent_position(positions_dict['middle_right'])
        positions_dict['middle'].add_adjacent_position(positions_dict['top_left'])
        positions_dict['middle'].add_adjacent_position(positions_dict['top_right'])
        positions_dict['middle'].add_adjacent_position(positions_dict['bottom_left'])
        positions_dict['middle'].add_adjacent_position(positions_dict['bottom_right'])

        positions_dict['outer_right'].add_adjacent_position(positions_dict['top_right'])
        positions_dict['outer_right'].add_adjacent_position(positions_dict['middle_right'])
        positions_dict['outer_right'].add_adjacent_position(positions_dict['bottom_right'])

        self.__positions = list(positions_dict.values())

    def __init_pieces(self):
        positions = self.__positions
        Piece(Animal.HOUND, positions[0])   # outer_left
        Piece(Animal.HOUND, positions[1])   # top_left
        Piece(Animal.HOUND, positions[3])   # bottom_left
        Piece(Animal.HARE, positions[10])   # outer_right

    def get_position(self, x: int, y: int):
        for position in self.__positions:
            distance = math.hypot(x - position.x, y - position.y)
            if distance <= self.__position_radius:
                return position

    def is_valid_move(self, from_position: Position, to_position: Position | None):
        if not to_position:
            return False

        piece = from_position.piece
        occupied = to_position.piece

        if (
            not piece
            or occupied
            or from_position == to_position
            or to_position not in from_position.adjacent_positions
        ):
            return False

        if piece.animal == Animal.HOUND and to_position.x < from_position.x:
            return False

        return True

    def move_piece(self, from_position: Position, to_position: Position):
        piece = from_position.piece
        piece.position = to_position
