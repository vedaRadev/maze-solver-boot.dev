from tkinter import Tk, BOTH, Canvas


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



def main():
    win = Window(800, 600)
    win.draw_line(0, 0, 800, 600, "red")

    cell_width = 30
    cell_height = 30
    topleft_x = 200
    topleft_y = 100

    cell = Cell(topleft_x, topleft_y, topleft_x + cell_width, topleft_y + cell_height)
    cell.has_right_wall = False
    cell.draw(win, "red")
    topleft_x += cell_width + 5

    cell = Cell(topleft_x, topleft_y, topleft_x + cell_width, topleft_y + cell_height)
    cell.draw(win, "red")
    topleft_x += cell_width + 5

    cell = Cell(topleft_x, topleft_y, topleft_x + cell_width, topleft_y + cell_height)
    cell.draw(win, "red")
    topleft_x += cell_width + 5

    cell = Cell(topleft_x, topleft_y, topleft_x + cell_width, topleft_y + cell_height)
    cell.has_top_wall = False
    cell.has_right_wall = False
    cell.draw(win, "red")
    topleft_x += cell_width + 5

    win.wait_for_close()

if __name__ == "__main__":
    main()
