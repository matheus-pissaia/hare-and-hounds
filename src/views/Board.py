import tkinter as tk

class Board():
    _tk: tk.Tk
    _canvas: tk.Canvas
    _nodes: list[tuple[float, float]]
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
    line_color = "#FFFFFF"    
    purple = "#9966FF"
    node_gap = 200
    window_width = 1280
    window_height = 720

    circle_radius = 40

    def __init__(self, nodes, tkinter : tk, canvas : tk.Canvas) -> None:
        self._nodes = nodes
        self._tk = tkinter
        self._canvas = canvas

    def draw_board(self):
        for edge in self.edges:
            node1 = self._nodes[edge[0]]
            node2 = self._nodes[edge[1]]
            self._canvas.create_line(
                node1[0], node1[1], node2[0], node2[1], width=8, fill=self.line_color
            )

        for x, y in self._nodes:
            self._canvas.create_oval(
                x - self.circle_radius,
                y - self.circle_radius,
                x + self.circle_radius,
                y + self.circle_radius,
                fill=self.purple,
                outline="",
            )