import math
from PIL import ImageTk, Image
import tkinter as tk
from enums.Animal import Animal
from models.Position import Position
from models.Piece import Piece


class Board:
    _positions: list[Position]

    #Atributos da implementacao visual
    _tk: tk.Tk
    _canvas: tk.Canvas
    _position_radius = 40
    """Radius of the position circle in px"""

    _gap_px = 200
    """Gap in pixels between positions"""

    _image_radius = 64
    _image_size = _image_radius * 2
    """Size of the image in px"""

    _hare_image: ImageTk.PhotoImage
    _hound_image: ImageTk.PhotoImage

    def __init__(self, tk_root: tk.Tk, canvas: tk.Canvas):
        self._tk = tk_root
        self._canvas = canvas

        self._init_images()
        self._init_positions()
        self._init_pieces()

    @property
    def positions(self):
        return self._positions

    @property
    def image_radius(self):
        return self._image_radius

    def draw_board(self):
        self._draw_edges()
        self._draw_positions()
        self._draw_pieces()

    def _init_images(self):
        """Initialize images once to avoid reloading every time."""
        self._hare_image = ImageTk.PhotoImage(
            Image.open("src/assets/hare.png").resize(
                (self._image_size, self._image_size)
            )
        )
        self._hound_image = ImageTk.PhotoImage(
            Image.open("src/assets/hound.png").resize(
                (self._image_size, self._image_size)
            )
        )

    def _draw_positions(self):
        for position in self._positions:
            self._canvas.create_oval(
                position.x - self._position_radius,
                position.y - self._position_radius,
                position.x + self._position_radius,
                position.y + self._position_radius,
                fill="black",
                outline="",
            )

    def _draw_edges(self):
        visited = set()

        for position in self._positions:
            visited.add(position)
            for adjacent_position in position.adjacent_positions:
                if adjacent_position not in visited:
                    self._canvas.create_line(
                        position.x,
                        position.y,
                        adjacent_position.x,
                        adjacent_position.y,
                        width=8,
                        fill="white",
                    )

    def _draw_pieces(self):
        for position in self._positions:
            piece = position.piece
            if piece:
                image = (
                    self._hare_image
                    if piece.animal == Animal.HARE
                    else self._hound_image
                )
                self._canvas.create_image(
                    position.x,
                    position.y,
                    anchor=tk.CENTER,
                    image=image,
                    tags="draggable",
                )

    def _init_positions(self):
        # Make sure to update TK before getting width and height
        self._tk.update()

        window_width = self._canvas.winfo_width()
        window_height = self._canvas.winfo_height()

        mid_x, mid_y = window_width / 2, window_height / 2

        positions_dict = {}

        # posicoes tabuleiro
        positions_dict['outer_left'] = Position(mid_x - (self._gap_px * 2), mid_y)
        positions_dict['top_left'] = Position(mid_x - self._gap_px, mid_y - self._gap_px)
        positions_dict['middle_left'] = Position(mid_x - self._gap_px, mid_y)
        positions_dict['bottom_left'] = Position(mid_x - self._gap_px, mid_y + self._gap_px)
        positions_dict['top'] = Position(mid_x, mid_y - self._gap_px)
        positions_dict['middle'] = Position(mid_x, mid_y)
        positions_dict['bottom'] = Position(mid_x, mid_y + self._gap_px)
        positions_dict['top_right'] = Position(mid_x + self._gap_px, mid_y - self._gap_px)
        positions_dict['middle_right'] = Position(mid_x + self._gap_px, mid_y)
        positions_dict['bottom_right'] = Position(mid_x + self._gap_px, mid_y + self._gap_px)
        positions_dict['outer_right'] = Position(mid_x + (self._gap_px * 2), mid_y)

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

        self._positions = list(positions_dict.values())

    def _init_pieces(self):
        positions = self._positions
        Piece(Animal.HOUND, positions[0])   # outer_left
        Piece(Animal.HOUND, positions[1])   # top_left
        Piece(Animal.HOUND, positions[3])   # bottom_left
        Piece(Animal.HARE, positions[10])   # outer_right

    def get_position(self, x: int, y: int):
        for position in self._positions:
            distance = math.hypot(x - position.x, y - position.y)
            if distance <= self._position_radius:
                return position
        return None

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

        if piece.animal == Animal.HOUND:
            if to_position.x < from_position.x:
                return False

        return True

    def move_piece(self, from_position: Position, to_position: Position):
        piece = from_position.piece
        piece.position = to_position
