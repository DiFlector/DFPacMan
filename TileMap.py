from random import random

import pygame
import Spritesheet
import sys
import World

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap:
    style = "spritesheet.png"

    def change_tile(self, index, value):
        temp = ""

        for i in range(868):
            if i != index:
                temp += self.str_map[i]
            else:
                temp += value

        self.str_map = temp

    def coins_generation(self):
        res = ''
        rand = random()
        for i in range(len(self.str_map)):
            if self.str_map[i] == '.' and random() <= 0.02 and i != 29:
                res += '@'
            elif self.str_map[i] == '.' and i != 29:
                res += '0'
            else:
                res += self.str_map[i]
        self.str_map = res

    def map_edit(self):
        res = ''
        indexes = [349, 350, 377, 378, 404, 405, 406, 407, 432, 433, 434, 435]
        curr = 0
        for i in range(len(self.str_map)):
            if (i == indexes[curr]):
                curr += 1
                if curr == 12:
                    curr = 11
                res += ':'
            else:
                res += self.str_map[i]
        self.str_map = res
        self.coins_generation()

    def __init__(self):
        tileMap = World.Map(16, 31, """
                    ||||||||||||||||
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |.........|||||:
                    |.........|||||:
                    *.........||||::
                    |.........||||::
                    |.........||||||
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    |...............
                    ||||||||||||||||
                    """)
        # verbosity option (-v)
        if len(sys.argv) > 1 and sys.argv[1] == "-v":
            tileMap.verbose = True

        # generate map by adding walls until there's no more room
        while tileMap.add_wall_obstacle(extend=True):
            pass

        self.str_map = ""
        for line in str(tileMap).splitlines():
            temp = []
            s = line[:14]
            self.str_map += s + s[::-1]

        self.map_edit()
        self.tile_size = 20
        self.start_x, self.start_y = 0, 0
        self.spritesheet = Spritesheet.Spritesheet(TileMap.style)
        self.tiles = self.load_tiles(self.str_map)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()
        self.coins_count = str.count(self.str_map, '0')

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def draw_map(self, surface):
        self.spritesheet = Spritesheet.Spritesheet(TileMap.style)
        self.tiles = self.load_tiles(self.str_map)
        self.load_map()
        surface.blit(self.map_surface, (0, 0))

    def load_tiles(self, map):
        tiles = []
        x, y = 0, 0

        i = 0
        for tile in map:
            if tile == ".":
                tiles.append(Tile("Floor.png", i % 28 * self.tile_size, i // 28 * self.tile_size, self.spritesheet))
            elif tile == "|":
                tiles.append(Tile("Wall.png", i % 28 * self.tile_size, i // 28 * self.tile_size, self.spritesheet))
            elif tile == "*":
                tiles.append(Tile("Portal.png", i % 28 * self.tile_size, i // 28 * self.tile_size, self.spritesheet))
            elif tile == ":":
                tiles.append(
                    Tile("GhostFloor.png", i % 28 * self.tile_size, i // 28 * self.tile_size, self.spritesheet))
            elif tile == "0":
                tiles.append(Tile("Coin.png", i % 28 * self.tile_size, i // 28 * self.tile_size, self.spritesheet))
            elif tile == "@":
                tiles.append(Tile("BigCoin.png", i % 28 * self.tile_size, i // 28 * self.tile_size, self.spritesheet))

            x, y = i % 28, i // 28
            i += 1

        x += 1
        y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size

        return tiles

    def get_tile(self, y, x):
        return self.str_map[y * 28 + x]
