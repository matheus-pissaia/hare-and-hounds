import tkinter as tk


class PlayerInterface:
    _tk: tk.Tk
    _canvas: tk.Canvas

    window_width = 1028
    window_height = 720
    middle = (window_width / 2, window_height / 2)
    node_gap = 200
    circle_radius = 40

    # Colors
    node_color_yellow = "#FFCC00"
    node_color_purple = "#9966FF"
    node_color_orange = "#FFA500"
    line_color = "#FFFFFF"

    # TODO improve positions calc
    # Node positions (X, Y)
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

    # TODO draw edges dynamically
    edges = [
        (0, 1),
        (0, 2),
        (0, 3),
        (2, 1),
        (2, 3),
        (4, 1),
        (4, 7),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 6),
        (5, 7),
        (5, 8),
        (5, 9),
        (6, 3),
        (6, 9),
        (8, 7),
        (8, 9),
        (10, 7),
        (10, 8),
        (10, 9),
    ]

    def __init__(self):
        self._tk = tk.Tk()
        self._canvas = tk.Canvas(
            self._tk, width=self.window_width, height=self.window_height, bg="#CCCCCC"
        )

        self._tk.title("Hare and Hounds")
        self._tk.wm_iconphoto(False, tk.PhotoImage(file="src/images/icon.png"))

        menubar = tk.Menu(self._tk)
        self._tk.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Exit", command=self._tk.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        self._canvas.pack()

    def draw_board(self):
        for edge in self.edges:
            node1 = self.nodes[edge[0]]
            node2 = self.nodes[edge[1]]
            self._canvas.create_line(
                node1[0], node1[1], node2[0], node2[1], width=8, fill=self.line_color
            )

        for x, y in self.nodes:
            self._canvas.create_oval(
                x - self.circle_radius,
                y - self.circle_radius,
                x + self.circle_radius,
                y + self.circle_radius,
                fill=self.node_color_purple,
                outline="",
            )

    def start(self):
        self.draw_board()
        self._tk.mainloop()
