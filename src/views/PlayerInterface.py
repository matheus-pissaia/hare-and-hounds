import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

from dog.start_status import StartStatus
from enums.GameMessages import GameMessages
from models.Position import Position
from views.Board import Board
from views.MenuBar import Menubar
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor


class PlayerInterface(DogPlayerInterface):
    __tk: tk.Tk
    __canvas: tk.Canvas
    __window_width = 1280
    __window_height = 720

    __board: Board
    __menubar: Menubar

    __game_info_frame: tk.Frame
    __game_messages: tk.Label
    __game_move_counter: tk.Label

    __dragging_item: tuple[int, Position] | None = None

    __dog_server_interface: DogActor

    def __init__(self):
        super().__init__()

        self.__init_window()
        self.__init_board_canvas()
        self.__init_game_info_frame()

        player_name = simpledialog.askstring(
            title="Player identification", prompt="Qual o seu nome?"
        )
        self.__dog_server_interface = DogActor()
        message = self.__dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)

    def start(self):
        self.__board.draw_board()
        self.__tk.mainloop()
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

    def __init_window(self):
        self.__tk = tk.Tk()
        self.__tk.resizable(False, False)
        self.__tk.title("Hare and Hounds")
        self.__tk.geometry(f"{self.__window_width}x{self.__window_height}")
        self.__tk.wm_iconphoto(False, tk.PhotoImage(file="src/images/icon.png"))

        self.__menubar = Menubar(self.__tk)
        self.__menubar.build_match_dropdown(self.start_match_command)

    def __init_board_canvas(self):
        self.__canvas = tk.Canvas(
            self.__tk, bg="#CCCCCC", height=self.__window_height * 0.85
        )

        self.__canvas.tag_bind("draggable", "<ButtonPress-1>", self.start_drag)
        self.__canvas.tag_bind("draggable", "<B1-Motion>", self.drag)
        self.__canvas.tag_bind("draggable", "<ButtonRelease-1>", self.end_drag)

        self.__canvas.pack(fill=tk.X, side=tk.TOP)

        self.__board = Board(self.__tk, self.__canvas)

    def __init_game_info_frame(self):
        self.__game_info_frame = tk.Frame(self.__tk, border=2, bg="#CCCCCC")

        # Create grid with 1 row and 2 columns with equal weight
        self.__game_info_frame.grid_rowconfigure(0, weight=1)
        self.__game_info_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        self.__game_info_frame.grid_columnconfigure(1, weight=1, uniform="equal")

        self.__game_move_counter = tk.Label(
            self.__game_info_frame,
            text="Movimentos: 0",
            anchor="center",
        )

        self.__game_messages = tk.Label(
            self.__game_info_frame,
            text=GameMessages.WELCOME.value,
            anchor="center",
        )

        self.__game_move_counter.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        self.__game_messages.grid(row=0, column=1, sticky="nsew", padx=(1, 0))

        self.__game_info_frame.pack(fill=tk.BOTH, expand=True)
