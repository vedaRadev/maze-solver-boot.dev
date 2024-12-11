from tkinter import Tk, BOTH, Canvas
from typing import Self


class Window:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title = "Maze Solver" # type: ignore
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(width = width, height = height)
        self.__canvas.pack()
        self.__running = False


    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()


    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
    

    def close(self):
        self.__running = False
    

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, fill_color: str):
        self.__canvas.create_line(x1, y1, x2, y2, fill = fill_color, width = 2)


class Cell:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
    

    def draw(self, window: Window, color: str):
        if self.has_left_wall:
            window.draw_line(self.__x1, self.__y1, self.__x1, self.__y2, color)
        if self.has_right_wall:
            window.draw_line(self.__x2, self.__y1, self.__x2, self.__y2, color)
        if self.has_top_wall:
            window.draw_line(self.__x1, self.__y1, self.__x2, self.__y1, color)
        if self.has_bottom_wall:
            window.draw_line(self.__x1, self.__y2, self.__x2, self.__y2, color)


    # TODO not a big fan of this API.
    # Maybe attach move drawing to the window class or just make it a standalone function?
    def draw_move(self, window: Window, other: Self, is_undo = False):
        color = "gray" if is_undo else "red"
        self_center_x = (self.__x1 + self.__x2) // 2
        self_center_y = (self.__y1 + self.__y2) // 2
        other_center_x = (other.__x1 + other.__x2) // 2
        other_center_y = (other.__y1 + other.__y2) // 2
        window.draw_line(self_center_x, self_center_y, other_center_x, other_center_y, color)



def main():
    window = Window(800, 600)
    window.draw_line(0, 0, 800, 600, "red")

    cell_width = 30
    cell_height = 30

    tl_x = 100
    tl_y = 100
    cell1 = Cell(tl_x, tl_y, tl_x + cell_width, tl_y + cell_height)

    tl_x = 100
    tl_y = 200
    cell2 = Cell(tl_x, tl_y, tl_x + cell_width, tl_y + cell_height)

    cell1.draw(window, "blue")
    cell2.draw(window, "blue")
    cell1.draw_move(window, cell2)

    window.wait_for_close()


if __name__ == "__main__":
    main()
