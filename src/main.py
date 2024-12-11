from tkinter import Tk, BOTH, Canvas
from typing import Callable
import time
from enum import Enum


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RUNNING = True


class Window:
    def __init__(self, width: int, height: int, on_close: Callable):
        self._width = width
        self._height = height
        self._root = Tk()
        self._root.title = "Maze Solver" # type: ignore
        self._root.protocol("WM_DELETE_WINDOW", on_close)
        self._canvas = Canvas(width = width, height = height)
        self._canvas.pack()


    def process_events(self):
        self._root.update_idletasks()
        self._root.update()


    def clear_color(self, color: str):
        self._canvas.create_rectangle(0, 0, self._width, self._height, fill = color)
    

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
        self.cells = []
        for y in range(self.num_rows):
            self.cells.append([])
            for _ in range(self.num_cols):
                self.cells[y].append(Cell())


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
                cell = self.cells[r][c]
                tl_x, tl_y, br_x, br_y = self.get_cell_screen_coords(r, c)
                cell.draw(window, "red", tl_x, tl_y, br_x, br_y)

    
def on_window_close():
    global RUNNING
    RUNNING = False


class SimulationState(Enum):
    BEGIN = "begin"
    BREAKING_ENTRANCE = "breaking entrance",
    BREAKING_EXIT = "breaking exit",
    DONE = "done"


def main():
    global RUNNING
    global SCREEN_WIDTH
    global SCREEN_HEIGHT

    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, on_window_close)

    # TODO math to center the maze on the screen
    cell_size = 50
    maze_offset = 10
    num_rows = (SCREEN_HEIGHT - maze_offset) // cell_size
    num_cols = (SCREEN_WIDTH - maze_offset) // cell_size
    maze = Maze(maze_offset, maze_offset, num_rows, num_cols, cell_size, cell_size)
    current_state = SimulationState.BEGIN
    while RUNNING:
        window.process_events()
        window.clear_color("black")

        # TODO cleaner state machine implementation
        match current_state:

            case SimulationState.BEGIN:
                # just for leaving one frame before breaking
                current_state = SimulationState.BREAKING_ENTRANCE

            case SimulationState.BREAKING_ENTRANCE:
                maze.cells[0][0].has_top_wall = False
                current_state = SimulationState.BREAKING_EXIT

            case SimulationState.BREAKING_EXIT:
                maze.cells[maze.num_rows - 1][maze.num_cols - 1].has_bottom_wall = False

            case SimulationState.DONE:
                pass # maze solved, nothing to do

        maze.draw_cells(window)
        time.sleep(0.05)


if __name__ == "__main__":
    main()
