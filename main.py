# Import Modules
import pygame


# Screen setup
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Finder")


# Colors
WHITE = (255, 255, 255)
BG_C = (30, 96, 145)
GRID_C = (24, 78, 119)
VISITED_C = (181, 228, 140)
QUEUE_C = (153, 217, 140)
START_C = (217, 237, 146)
END_C = (118, 200, 147)
SOLVED_C = (26, 117, 159)


# Grid
COLS, ROWS = 50, 50
BOX_WIDTH = WIDTH // COLS
BOX_HEIGHT = HEIGHT // ROWS

grid = []
queue = []
path = []


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.end = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * BOX_WIDTH, self.y * BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < COLS - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < ROWS - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


def get_clicked_pos(pos):
    x, y = pos

    row = x // BOX_WIDTH
    col = y // BOX_HEIGHT
    return row, col


def draw_grid(win, cols, rows, width, height):
    for row in range(rows):
        pygame.draw.line(win, GRID_C, (0, row * BOX_HEIGHT), (width, row * BOX_HEIGHT))
        for col in range(cols):
            pygame.draw.line(win, GRID_C, (col * BOX_WIDTH, 0), (col * BOX_WIDTH, height))


def draw_win(win, cols, rows, width, height):

    win.fill(BG_C)

    for col in range(cols):
        for row in range(rows):
            box = grid[col][row]

            box.draw(win, BG_C)

            if box.queued:
                box.draw(win, QUEUE_C)

            if box.visited:
                box.draw(win, VISITED_C)

            if box in path:
                box.draw(win, SOLVED_C)

            if box.start:
                box.draw(win, START_C)

            if box.end:
                box.draw(win, END_C)

            if box.wall:
                box.draw(win, WHITE)

    draw_grid(win, cols, rows, width, height)

    pygame.display.update()


def algorithm(start_box, end_box):
    if len(queue) > 0:
        current_box = queue.pop(0)
        current_box.visited = True
        if current_box == end_box:
            while current_box.prior != start_box:
                path.append(current_box.prior)
                current_box = current_box.prior
            return True
        else:
            for neighbour in current_box.neighbours:
                if not neighbour.queued and not neighbour.wall:
                    neighbour.queued = True
                    neighbour.prior = current_box
                    queue.append(neighbour)


# Build Grid
for i in range(COLS):
    arr = []
    for j in range(ROWS):
        arr.append(Box(i, j))
    grid.append(arr)

# Set Neighbours
for i in range(COLS):
    for j in range(ROWS):
        grid[i][j].set_neighbours()


def main():

    start_box = None
    end_box = None

    run = True
    begin = False
    searching = True

    while run:

        draw_win(WIN, COLS, ROWS, WIDTH, HEIGHT)

        for event in pygame.event.get():
            # QUIT window
            if event.type == pygame.QUIT:
                run = False

            if begin:
                continue

            if pygame.mouse.get_pressed()[0]:  # Checks if the left mouse button is pressed
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                box = grid[row][col]

                if not start_box:
                    start_box = box
                    start_box.start = True
                    start_box.visited = True
                    queue.append(start_box)

                elif box != start_box and not end_box:
                    end_box = box
                    end_box.end = True

                elif box != end_box and box != start_box:
                    box.wall = True

            elif pygame.mouse.get_pressed()[2]:  # Check if right mouse button pressed
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                box = grid[row][col]

                if box == start_box:
                    start_box.start = False
                    start_box.visited = False
                    start_box = None
                    queue.remove(box)
                elif box == end_box:
                    end_box.end = False
                    end_box = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not begin:
                    begin = True

        if begin:
            if searching:
                if algorithm(start_box, end_box):
                    searching = False

    pygame.quit()


main()
