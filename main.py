import pygame
import sys
import os
import random
import threading

colours = {
    "cream": (238, 228, 218),
    "light_gray": (119, 110, 101),
    "light_brown": (205, 193, 180),
    "dark_brown": (187, 173, 160),
    "white": (250, 248, 239),
}

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Fifteen Puzzle")
clock = pygame.time.Clock()
pygame.init()

default_font = pygame.font.Font(
    os.path.join(os.path.dirname(__file__), "assets/montserrat_regular.ttf"), 36
)
bold_font = pygame.font.Font(
    os.path.join(os.path.dirname(__file__), "assets/montserrat_bold.ttf"), 36
)


class Tile:
    def __init__(self, position, size, number):
        self.position = position
        self.number = number
        self.size = size

    def draw(self):
        if self.number != "":
            pygame.draw.rect(
                screen,
                colours["cream"],
                (self.position[0], self.position[1], self.size, self.size),
                border_radius=5,
            )
            text = bold_font.render(str(self.number), True, colours["light_gray"])
            text_rect = text.get_rect(
                center=(
                    self.position[0] + self.size // 2,
                    self.position[1] + self.size // 2,
                )
            )
            screen.blit(text, text_rect)
        else:
            pygame.draw.rect(
                screen,
                colours["light_brown"],
                (self.position[0], self.position[1], self.size, self.size),
                border_radius=5,
            )


class Grid:
    def __init__(self, size, position):
        self.size = size
        self.position = position
        self.line_space = 15
        self.moves = 0
        self.tile_size = (self.size - 5 * self.line_space) // 4
        self.tiles = self.generate_tiles()
        self.original_state = [tile.position for tile in self.tiles]
        self.scramble(200)

    def draw_grid(self, move_pos=(150, 150)):
        screen.fill(colours["white"])
        mov_surf = default_font.render(
            f"Moves: {self.moves}", True, colours["light_gray"]
        )
        screen.blit(mov_surf, move_pos)
        pygame.draw.rect(
            screen,
            colours["dark_brown"],
            (self.position[0], self.position[1], self.size, self.size),
            border_radius=5,
        )
        for tile in self.tiles:
            tile.draw()

    def generate_tiles(self):
        tiles = [
            Tile(
                (
                    self.position[0]
                    + self.line_space
                    + 3 * (self.tile_size + self.line_space),
                    self.position[1]
                    + self.line_space
                    + 3 * (self.tile_size + self.line_space),
                ),
                self.tile_size,
                "",
            )
        ]
        for j in range(4):
            for i in range(4):
                num = j * 4 + i + 1
                if num < 16:
                    tiles.append(
                        Tile(
                            (
                                self.position[0]
                                + self.line_space
                                + i * (self.tile_size + self.line_space),
                                self.position[1]
                                + self.line_space
                                + j * (self.tile_size + self.line_space),
                            ),
                            self.tile_size,
                            num,
                        )
                    )
        return tiles

    def set_solved_state(self):
        for index, tile in enumerate(self.tiles):
            tile.position = self.original_state[index]

    def scramble(self, moves):
        self.set_solved_state()
        for _ in range(moves):
            empty_tile = [t for t in self.tiles if t.number == ""][0]
            dirs = []
            r = (empty_tile.position[1] - self.position[1] - self.line_space) // (
                self.tile_size + self.line_space
            )
            c = (empty_tile.position[0] - self.position[0] - self.line_space) // (
                self.tile_size + self.line_space
            )
            if r > 0:
                dirs.append("down")
            if r < 3:
                dirs.append("up")
            if c > 0:
                dirs.append("right")
            if c < 3:
                dirs.append("left")
            direction = random.choice(dirs)
            self.move(direction, animate=False)
        self.moves = 0

    def animate(self, pos1, pos2, frames=10):
        original_pos1 = pos1.position
        original_pos2 = pos2.position
        pos2.position = original_pos1
        self.tiles.insert(0, Tile(original_pos2, self.tile_size, pos2.number))
        x1, y1 = original_pos1
        x2, y2 = original_pos2
        dx = (x2 - x1) / frames
        dy = (y2 - y1) / frames
        for _ in range(frames):
            self.draw_grid()
            x1 += dx
            y1 += dy
            pos1.position = (x1, y1)
            pygame.display.flip()
            clock.tick(60)
        pos1.position = original_pos2
        pos2.position = original_pos1
        self.tiles.pop(0)

    def move(self, direction, animate=True):
        empty_tile = [tile for tile in self.tiles if tile.number == ""][0]
        neighbour = self.get_neighbour(direction, empty_tile)
        if neighbour:
            if animate:
                self.animate(neighbour[0], empty_tile)
            else:
                pos1 = neighbour[0].position
                pos2 = empty_tile.position
                neighbour[0].position, empty_tile.position = pos2, pos1
            self.moves += 1
        self.draw_grid()

    def check_win(self):
        return [tile.position for tile in self.tiles] == self.original_state

    def get_neighbour(self, direction, empty_tile):
        if direction == "up":
            return [
                tile
                for tile in self.tiles
                if tile.position
                == (
                    empty_tile.position[0],
                    empty_tile.position[1] + empty_tile.size + self.line_space,
                )
            ]
        elif direction == "down":
            return [
                tile
                for tile in self.tiles
                if tile.position
                == (
                    empty_tile.position[0],
                    empty_tile.position[1] - empty_tile.size - self.line_space,
                )
            ]
        elif direction == "left":
            return [
                tile
                for tile in self.tiles
                if tile.position
                == (
                    empty_tile.position[0] + empty_tile.size + self.line_space,
                    empty_tile.position[1],
                )
            ]
        elif direction == "right":
            return [
                tile
                for tile in self.tiles
                if tile.position
                == (
                    empty_tile.position[0] - empty_tile.size - self.line_space,
                    empty_tile.position[1],
                )
            ]


class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.goal = self.get_goal_state()
        self.solving = False
        self.done = False
        self.path = None

    def get_goal_state(self):
        arr = [None] * 16
        for i, pos in enumerate(self.grid.original_state):
            r = (pos[1] - self.grid.position[1] - self.grid.line_space) // (
                self.grid.tile_size + self.grid.line_space
            )
            c = (pos[0] - self.grid.position[0] - self.grid.line_space) // (
                self.grid.tile_size + self.grid.line_space
            )
            arr[r * 4 + c] = i
        return tuple(arr)

    def get_current_state(self):
        arr = [None] * 16
        for i, tile in enumerate(self.grid.tiles):
            r = (tile.position[1] - self.grid.position[1] - self.grid.line_space) // (
                self.grid.tile_size + self.grid.line_space
            )
            c = (tile.position[0] - self.grid.position[0] - self.grid.line_space) // (
                self.grid.tile_size + self.grid.line_space
            )
            arr[r * 4 + c] = i
        return tuple(arr)

    def manhattan_distance(self, idx, tile_id):
        goal_idx = self.goal.index(tile_id)
        r1, c1 = idx // 4, idx % 4
        r2, c2 = goal_idx // 4, goal_idx % 4
        return abs(r1 - r2) + abs(c1 - c2)

    def linear_conflicts(self, state):
        conflicts = 0
        for row_start in range(0, 16, 4):
            row = state[row_start : row_start + 4]
            for i in range(4):
                for j in range(i + 1, 4):
                    tile_i = row[i]
                    tile_j = row[j]
                    if tile_i != 0 and tile_j != 0:
                        goal_i = self.goal.index(tile_i)
                        goal_j = self.goal.index(tile_j)
                        if (
                            (goal_i // 4 == goal_j // 4)
                            and tile_i > tile_j
                            and (row_start // 4 == goal_i // 4)
                        ):
                            conflicts += 2
        for col_start in range(4):
            col = [state[col_start + 4 * i] for i in range(4)]
            for i in range(4):
                for j in range(i + 1, 4):
                    tile_i = col[i]
                    tile_j = col[j]
                    if tile_i != 0 and tile_j != 0:
                        goal_i = self.goal.index(tile_i)
                        goal_j = self.goal.index(tile_j)
                        if (
                            (goal_i % 4 == goal_j % 4)
                            and tile_i > tile_j
                            and (col_start == goal_i % 4)
                        ):
                            conflicts += 2
        return conflicts

    def heuristic(self, state):
        cost = 0
        for idx, tile_id in enumerate(state):
            if tile_id != 0:
                cost += self.manhattan_distance(idx, tile_id)
        cost += self.linear_conflicts(state)
        return cost

    def get_neighbors(self, state):
        neighbors = []
        blank_index = state.index(0)
        r, c = blank_index // 4, blank_index % 4
        moves = [
            ("down", (-1, 0)),
            ("up", (1, 0)),
            ("right", (0, -1)),
            ("left", (0, 1)),
        ]
        for move_dir, (dr, dc) in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 4 and 0 <= nc < 4:
                new_state = list(state)
                new_state[blank_index], new_state[nr * 4 + nc] = (
                    new_state[nr * 4 + nc],
                    new_state[blank_index],
                )
                neighbors.append((move_dir, tuple(new_state)))
        return neighbors

    def search(self, path, g, bound, moves):
        node = path[-1]
        f = g + self.heuristic(node)
        if f > bound:
            return f
        if node == self.goal:
            return "FOUND"
        mn = float("inf")
        for move_dir, nxt in self.get_neighbors(node):
            if nxt not in self.visited:
                self.visited.add(nxt)
                path.append(nxt)
                moves.append(move_dir)
                t = self.search(path, g + 1, bound, moves)
                if t == "FOUND":
                    return "FOUND"
                if isinstance(t, int) and t < mn:
                    mn = t
                path.pop()
                moves.pop()
                self.visited.remove(nxt)
        return mn

    def ida_star(self, start):
        bound = self.heuristic(start)
        path = [start]
        moves = []
        while True:
            self.visited = {start}
            t = self.search(path, 0, bound, moves)
            if t == "FOUND":
                return moves
            if t == float("inf"):
                return None
            bound = t

    def _solve_background(self):
        st = self.get_current_state()
        self.path = self.ida_star(st)
        self.solving = False
        self.done = True

    def start_solve(self):
        if not self.solving and not self.done:
            self.solving = True
            threading.Thread(target=self._solve_background, daemon=True).start()

    def apply_solution(self):
        if self.path:
            for move_dir in self.path:
                self.grid.move(move_dir)
        self.path = None
        self.done = False


game = Grid(500, (150, 200))
solver = Solver(game)
won = False

while True:
    game.draw_grid()
    msg = None

    if solver.solving:
        dots = (pygame.time.get_ticks() // 500) % 3
        msg = "Solving" + "." * (dots + 1)

    if solver.done:
        solver.apply_solution()

    if game.check_win():
        msg = f"You Won in {game.moves} moves!"
        won = True

    if msg:
        text_surf = bold_font.render(msg, True, colours["light_gray"])
        screen.blit(
            text_surf, (screen.get_width() // 2 - text_surf.get_width() // 2, 50)
        )

    if won:
        prompt_surf = bold_font.render(
            "Press SPACE to scramble again", True, colours["light_gray"]
        )
        screen.blit(
            prompt_surf, (screen.get_width() // 2 - prompt_surf.get_width() // 2, 90)
        )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.scramble(200)
                if won:
                    game.moves = 0
                    won = False
                solver.solving = False
                solver.done = False
                solver.path = None
            elif event.key == pygame.K_s:
                if not solver.solving and not won:
                    solver.start_solve()
            if not won and not solver.solving:
                if event.key == pygame.K_UP:
                    game.move("up")
                elif event.key == pygame.K_DOWN:
                    game.move("down")
                elif event.key == pygame.K_LEFT:
                    game.move("left")
                elif event.key == pygame.K_RIGHT:
                    game.move("right")

    pygame.display.flip()
    clock.tick(30)
