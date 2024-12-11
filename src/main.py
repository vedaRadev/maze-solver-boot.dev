from tkinter import Tk, BOTH, Canvas
from typing import Self
import time


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Window:
    def __init__(self, width: int, height: int):
        self._root = Tk()
        self._root.title = "Maze Solver" # type: ignore
        self._root.protocol("WM_DELETE_WINDOW", self.close)
        self._canvas = Canvas(width = width, height = height)
        self._canvas.pack()
        self._running = False


    def redraw(self):
        self._root.update_idletasks()
        self._root.update()


    def wait_for_close(self):
        self._running = True
        while self._running:
            self.redraw()
    

    def close(self):
        self._running = False
    

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, fill_color: str):
        self._canvas.create_line(x1, y1, x2, y2, fill = fill_color, width = 2)


class Cell:
    def __init__(self):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
    

    def draw(self, window: Window, color: str, x1: int, y1: int, x2: int, y2: int):
        if self.has_left_wall:
            window.draw_line(x1, y1, x1, y2, color)
        if self.has_right_wall:
            window.draw_line(x2, y1, x2, y2, color)
        if self.has_top_wall:
            window.draw_line(x1, y1, x2, y1, color)
        if self.has_bottom_wall:
            window.draw_line(x1, y2, x2, y2, color)


class Maze:
    def __init__(
        self,
        x1: int, y1: int,
        num_rows: int, num_cols: int,
        cell_width: int, cell_height: int
    ): 
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.generate_cells()


    def generate_cells(self):
        self._cells = []
        for y in range(self.num_rows):
            self._cells.append([])
            for _ in range(self.num_cols):
                self._cells[y].append(Cell())


    # TODO check that the row, col pair is in bounds of the cells matrix
    def get_cell_screen_coords(self, row: int, col: int) -> tuple[int, int, int, int]:
        cell_topleft_x = self.x1 + col * self.cell_width
        cell_topleft_y = self.y1 + row * self.cell_height
        cell_bottomright_x = cell_topleft_x + self.cell_width
        cell_bottomright_y = cell_topleft_y + self.cell_height
        return (cell_topleft_x, cell_topleft_y, cell_bottomright_x, cell_bottomright_y)


    def draw_move(self, window: Window, a_row: int, a_col: int, b_row: int, b_col: int, is_undo = False):
        color = "gray" if is_undo else "red"
        a_tl_x, a_tl_y, a_br_x, a_br_y = self.get_cell_screen_coords(a_row, a_col)
        a_center_x = (a_tl_x + a_br_x) // 2
        a_center_y = (a_tl_y + a_br_y) // 2

        b_tl_x, b_tl_y, b_br_x, b_br_y = self.get_cell_screen_coords(b_row, b_col)
        b_center_x = (b_tl_x + b_br_x) // 2
        b_center_y = (b_tl_y + b_br_y) // 2

        window.draw_line(a_center_x, a_center_y, b_center_x, b_center_y, color)


    def draw_cells(self, window: Window):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                cell = self._cells[r][c]
                tl_x, tl_y, br_x, br_y = self.get_cell_screen_coords(r, c)
                cell.draw(window, "red", tl_x, tl_y, br_x, br_y)

    
    # def animate(self, window: Window):
    #     window.redraw()
    #     time.sleep(0.05)


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT)

    # TODO math to center the maze on the screen
    cell_size = 50
    maze_offset = 10
    num_rows = (SCREEN_HEIGHT - maze_offset) // cell_size
    num_cols = (SCREEN_WIDTH - maze_offset) // cell_size

    maze = Maze(maze_offset, maze_offset, num_rows, num_cols, cell_size, cell_size)
    maze.draw_cells(window)

    window.wait_for_close()


if __name__ == "__main__":
    main()
