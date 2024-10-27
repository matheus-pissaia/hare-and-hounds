import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from typing import Literal

from dog.dog_actor import DogActor
from dog.start_status import StartStatus
from dog.dog_interface import DogPlayerInterface

from views.Board import Board
from views.MenuBar import Menubar
from models.Position import Position
from enums.GameMessages import GameMessages


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

    def start_match_command(self):
        # Do nothing if the game already started
        if self.__board.is_match_in_progress():
            return

        answer = messagebox.askyesno("START", "Deseja iniciar uma nova partida?")

        # Do nothing if player do not want to start a match
        if not answer:
            return

        # Start a new match with 2 players
        start_status = self.__dog_server_interface.start_match(2)
        code = start_status.get_code()
        message = start_status.get_message()

        if code == "0" or code == "1":
            messagebox.showinfo(message=message)
        else:
            self.setup_game()
            self.__board.start_match(start_status.get_players())

            messagebox.showinfo(message=start_status.get_message())

        if self.__board.is_local_player_turn():
            self.show_game_info_message(GameMessages.START_DRAG)

        else:
            self.show_game_info_message(GameMessages.WAITING_OPPONENT)

    def receive_start(self, start_status: StartStatus):
        self.setup_game()
        self.__board.start_match(start_status.get_players())

        if self.__board.is_local_player_turn():
            self.show_game_info_message(GameMessages.START_DRAG)

        else:
            self.show_game_info_message(GameMessages.WAITING_OPPONENT)

    def setup_game(self):
        self.__board.reset()
        self.update_menubar()

    def start_drag(self, event: tk.Event):
        # Disable dragging if it is not local player turn
        if not self.__board.is_local_player_turn():
            return

        item = self.__canvas.find_withtag(tk.CURRENT)

        if not item or len(item) == 0:
            return

        coord = self.__canvas.coords(item[0])
        from_position = self.__board.get_position(coord[0], coord[1])

        if not from_position or not from_position.piece:
            return

        # Check if chosen piece belongs to local player
        if self.__board.is_local_player_piece(from_position.piece):
            self.__dragging_item = (item[0], from_position)

        else:
            self.show_game_info_message(GameMessages.INVALID_PIECE)

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
            self.show_game_info_message(GameMessages.INVALID_MOVE)
            # Return piece back to initial position
            self.update_piece_screen_position(from_position.x, from_position.y)

        else:
            move_to_send = self.__board.move_piece(from_position, to_position)

            self.update_move_counter()
            self.update_piece_screen_position(to_position.x, to_position.y)

            self.__dog_server_interface.send_move(move_to_send)

            animal_winner = move_to_send["winner"]
            game_message = GameMessages.WAITING_OPPONENT

            if animal_winner:
                if self.__board.is_local_player_winner():
                    game_message = GameMessages.YOU_WIN

                else:
                    game_message = GameMessages.YOU_LOSE

            self.show_game_info_message(game_message)

        self.__dragging_item = None

    def update_piece_screen_position(
        self,
        x: int,
        y: int,
        item_id: int | None = None,
    ):
        if not item_id and not self.__dragging_item:
            return

        self.__canvas.moveto(
            item_id or self.__dragging_item[0],
            x - self.__board.image_radius,
            y - self.__board.image_radius,
        )

    def update_menubar(self):
        if self.__board.is_match_in_progress():
            self.__menubar.match_dropdown.entryconfigure(
                "Iniciar partida", state="disabled"
            )
        else:
            self.__menubar.match_dropdown.entryconfigure(
                "Iniciar partida", state="normal"
            )

    def update_move_counter(self):
        self.__board.increase_move_counter()
        self.__game_move_counter["text"] = f"Movimentos: {self.__board.move_counter}"

    def receive_move(self, move: dict):
        to_pos_coord: list[int] = move["to_pos"]
        from_pos_coord: list[int] = move["from_pos"]
        match_status: Literal["next", "finished"] = move["match_status"]
        animal_winner: str | None = move["winner"]

        to_pos = self.__board.get_position(to_pos_coord[0], to_pos_coord[1])
        from_pos = self.__board.get_position(from_pos_coord[0], from_pos_coord[1])

        # Check if positions exist and if "from_pos" has a piece
        if not from_pos or not from_pos.piece or not to_pos:
            return

        # Find closest piece from "from_pos"
        item = self.__canvas.find_closest(from_pos.x, from_pos.y)

        if not item or len(item) == 0:
            return

        self.__board.move_piece(from_pos, to_pos)

        self.update_move_counter()
        self.update_piece_screen_position(to_pos.x, to_pos.y, item[0])

        game_message = GameMessages.YOUR_TURN

        if match_status == "finished" and animal_winner:
            self.__board.set_winner(animal_winner)

            if self.__board.is_local_player_winner():
                game_message = GameMessages.YOU_WIN

            else:
                game_message = GameMessages.YOU_LOSE

        self.show_game_info_message(game_message)

    def receive_withdrawal_notification(self):
        self.show_game_info_message(GameMessages.ABANDONED)
        self.__board.receive_withdrawal_notification()
        self.update_menubar()

    def show_game_info_message(self, message: GameMessages):
        self.__game_messages["text"] = message.value

        foreground_color = "black"

        if message == GameMessages.YOU_WIN:
            foreground_color = "green"

        elif message == GameMessages.INVALID_MOVE or message == GameMessages.YOU_LOSE:
            foreground_color = "red"

        self.__game_messages["foreground"] = foreground_color

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
