from enum import Enum
import pygame
import time
import random


class Cell:
    def __init__(self):
        self.visited = False
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
    

    def draw(self, screen: pygame.Surface, color: str, x1: int, y1: int, x2: int, y2: int):
        if self.has_left_wall:
            pygame.draw.line(screen, color, (x1, y1), (x1, y2))
        if self.has_right_wall:
            pygame.draw.line(screen, color, (x2, y1), (x2, y2))
        if self.has_top_wall:
            pygame.draw.line(screen, color, (x1, y1), (x2, y1))
        if self.has_bottom_wall:
            pygame.draw.line(screen, color, (x1, y2), (x2, y2))


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
    

    def draw_move(self, screen: pygame.Surface, a_row: int, a_col: int, b_row: int, b_col: int, is_undo = False):
        color = "gray" if is_undo else "red"
        a_tl_x, a_tl_y, a_br_x, a_br_y = self.get_cell_screen_coords(a_row, a_col)
        a_center_x = (a_tl_x + a_br_x) // 2
        a_center_y = (a_tl_y + a_br_y) // 2

        b_tl_x, b_tl_y, b_br_x, b_br_y = self.get_cell_screen_coords(b_row, b_col)
        b_center_x = (b_tl_x + b_br_x) // 2
        b_center_y = (b_tl_y + b_br_y) // 2

        pygame.draw.line(screen, color, (a_center_x, a_center_y), (b_center_x, b_center_y))


    def draw_cells(self, screen: pygame.Surface):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                cell = self.cells[r][c]
                tl_x, tl_y, br_x, br_y = self.get_cell_screen_coords(r, c)
                cell.draw(screen, "green", tl_x, tl_y, br_x, br_y)

    
class SimulationState(Enum):
    BEGIN = "begin"
    BREAKING_ENTRANCE = "breaking entrance"
    BREAKING_EXIT = "breaking exit"
    GENERATING_MAZE = "generating_maze"
    DONE = "done"


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    random.seed(None)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # TODO math to center the maze on the screen
    cell_size = 50
    maze_offset = 10
    num_rows = (SCREEN_HEIGHT - maze_offset) // cell_size
    num_cols = (SCREEN_WIDTH - maze_offset) // cell_size
    maze = Maze(maze_offset, maze_offset, num_rows, num_cols, cell_size, cell_size)

    # start at top-right, perform DFS using this stack to generate the maze
    gen_stack = [((0, 0), [])]
    current_state = SimulationState.BEGIN
    while True:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                return

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
                current_state = SimulationState.GENERATING_MAZE

            case SimulationState.GENERATING_MAZE:
                if not gen_stack:
                    for row in maze.cells:
                        for cell in row:
                            cell.visited = False
                    current_state = SimulationState.DONE
                    continue

                (x, y), can_visit = gen_stack[-1]
                if not maze.cells[y][x].visited:
                    maze.cells[y][x].visited = True
                    if y - 1 >= 0 and not maze.cells[y - 1][x].visited:
                        can_visit.append(Direction.UP)
                    if y + 1 < maze.num_rows and not maze.cells[y + 1][x].visited:
                        can_visit.append(Direction.DOWN)
                    if x - 1 >= 0 and not maze.cells[y][x - 1].visited:
                        can_visit.append(Direction.LEFT)
                    if x + 1 < maze.num_cols and not maze.cells[y][x + 1].visited:
                        can_visit.append(Direction.RIGHT)

                # we've exhausted all possible directions
                if not can_visit:
                    gen_stack.pop()
                    continue

                match can_visit.pop(random.randrange(0, len(can_visit))):
                    case Direction.UP:
                        next_x = x
                        next_y = y - 1
                        if maze.cells[next_y][next_x].visited: continue
                        maze.cells[y][x].has_top_wall = False
                        maze.cells[next_y][next_x].has_bottom_wall = False
                        gen_stack.append(((next_x, next_y), []))
                    case Direction.RIGHT:
                        next_x = x + 1
                        next_y = y
                        if maze.cells[next_y][next_x].visited: continue
                        maze.cells[y][x].has_right_wall = False
                        maze.cells[next_y][next_x].has_left_wall = False
                        gen_stack.append(((next_x, next_y), []))
                    case Direction.DOWN:
                        next_x = x
                        next_y = y + 1
                        if maze.cells[next_y][next_x].visited: continue
                        maze.cells[y][x].has_bottom_wall = False
                        maze.cells[next_y][next_x].has_top_wall = False
                        gen_stack.append(((next_x, next_y), []))
                    case Direction.LEFT:
                        next_x = x - 1
                        next_y = y
                        if maze.cells[next_y][next_x].visited: continue
                        maze.cells[y][x].has_left_wall = False
                        maze.cells[next_y][next_x].has_right_wall = False
                        gen_stack.append(((next_x, next_y), []))


            case SimulationState.DONE:
                pass # maze solved, nothing to do

        screen.fill("black")
        maze.draw_cells(screen)
        pygame.display.flip()
        # FIXME sleeping the thread means we might miss events such as the user clicking the
        # window's close button!
        time.sleep(0.03)


if __name__ == "__main__":
    main()
