import pygame
import sys
from colours import *
import os
import random

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Fifteen Puzzle")
clock = pygame.time.Clock()
pygame.init()

default_font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets/montserrat_regular.ttf"), 36)
bold_font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "assets/montserrat_bold.ttf"), 36)

class Tile:
    def __init__(self, position, size, number):
        self.position = position
        self.number = number
        self.size = size

    def draw(self):
        if not self.number == "":
            pygame.draw.rect(screen, colours["cream"], (self.position[0], self.position[1], self.size, self.size), border_radius=5)
            text = bold_font.render(str(self.number), True, colours["light_gray"])
            text_rect = text.get_rect(center=(self.position[0] + self.size // 2, self.position[1] + self.size // 2))
            screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, colours["light_brown"], (self.position[0], self.position[1], self.size, self.size), border_radius=5)

class Grid:
    def __init__(self, size, position):
        self.size = size
        self.position = position
        self.line_space = 15
        self.moves = 0
        self.tile_size = (self.size - 5*self.line_space)//4
        self.tiles = self.generate_tiles()
        self.original_state = [tile.position for tile in self.tiles]
        self.shuffle()

    def draw_grid(self):
        pygame.draw.rect(screen, colours["dark_brown"], (self.position[0], self.position[1], self.size, self.size), border_radius=5)
        for tile in self.tiles:
            tile.draw()

    def generate_tiles(self):
        tiles = [Tile((self.position[0] + self.line_space + 3 * (self.tile_size+self.line_space), self.position[1] + self.line_space + 3 * (self.tile_size+self.line_space)), self.tile_size, "")]
        for i in range(4):
            for j in range(4):
                num = i + j * 4 + 1
                if num < 16:
                    tiles.append(Tile((self.position[0] + self.line_space + i * (self.tile_size+self.line_space), self.position[1] + self.line_space + j * (self.tile_size+self.line_space)), self.tile_size, num))
        return tiles
    
    def shuffle(self):
        while True:
            numbers = [tile.number for tile in self.tiles]
            random.shuffle(numbers)
            inversions = 0
            for i in range(len(numbers)):
                for j in range(i + 1, len(numbers)):
                    if numbers[i] != "" and numbers[j] != "" and numbers[i] > numbers[j]:
                        inversions += 1
            blank_tile = next(tile for tile in self.tiles if tile.number == "")
            blank_row = 4 - (self.tiles.index(blank_tile) // 4)
            if (inversions + blank_row) % 2 == 0:
                break

        positions = [tile.position for tile in self.tiles]
        for tile in self.tiles:
            tile.position = positions[numbers.index(tile.number)]


    def animate(self, pos1, pos2, frames=200):
        original_pos1 = pos1.position
        original_pos2 = pos2.position
        pos2.position = original_pos1
        self.tiles.insert(0, (Tile(original_pos2, self.tile_size, pos2.number)))
        x1, y1 = original_pos1
        x2, y2 = original_pos2
        dx = (x2-x1)/frames
        dy = (y2-y1)/frames
        for _ in range(frames):
            self.draw_grid()
            x1 += dx
            y1 += dy
            pos1.position = (x1, y1)
            pygame.display.flip()
        pos1.position = original_pos2
        pos2.position = original_pos1
        self.tiles.pop(0)

    def move(self, direction):
        empty_tile = [tile for tile in self.tiles if tile.number == ""][0]
        neighbour = self.get_neighbour(direction, empty_tile)
        if neighbour:
            self.animate(neighbour[0], empty_tile)
            self.moves += 1
        self.draw_grid()
    
    def check_win(self):
        return [tile.position for tile in self.tiles] == self.original_state
    
    def get_neighbour(self, direction, empty_tile):
        if direction == "up":
            return [tile for tile in self.tiles if tile.position == (empty_tile.position[0], empty_tile.position[1] + empty_tile.size + self.line_space)]
        elif direction == "down":
            return [tile for tile in self.tiles if tile.position == (empty_tile.position[0], empty_tile.position[1] - empty_tile.size - self.line_space)]
        elif direction == "left":
            return [tile for tile in self.tiles if tile.position == (empty_tile.position[0] + empty_tile.size + self.line_space, empty_tile.position[1])]
        elif direction == "right":
            return [tile for tile in self.tiles if tile.position == (empty_tile.position[0] - empty_tile.size - self.line_space, empty_tile.position[1])]
        
class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.open = []
        self.closed = [] 

    def solve(self):
        pass
        
                 
game = Grid(500, (150, 200))
won = False

while True:
    screen.fill(colours["white"])
    game.draw_grid()
    screen.blit(default_font.render(f"Moves: {game.moves}", True, colours["light_gray"]), (150, 150))
    if game.check_win():
        screen.blit(bold_font.render(f"You Won in {game.moves} moves!", True, colours["light_gray"]), (screen.get_width()//2 - 190, 50))
        screen.blit(bold_font.render("Press SPACE to shuffle", True, colours["light_gray"]), (screen.get_width()//2 - 205, 90))
        won = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.shuffle()
                if won:
                    game.moves = 0
                    won = False
            if not won:
                if event.key == pygame.K_UP:
                    game.move("up")
                if event.key == pygame.K_DOWN:
                    game.move("down")
                if event.key == pygame.K_LEFT:
                    game.move("left")
                if event.key == pygame.K_RIGHT:
                    game.move("right")

    pygame.display.flip()
    clock.tick(30)