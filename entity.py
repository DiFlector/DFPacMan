import cmath
import sys
import random
from itertools import count

import pygame
import pygame.surface
import element

from TileMap import TileMap

WIDTH = 560
HEIGHT = 620
clock = pygame.time.Clock()

# test
class Entity(pygame.sprite.Sprite):
    save_image = 0
    key_w = False
    key_s = False
    key_a = False
    key_d = False

    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image = pygame.image.load(img).convert_alpha()
        self.save_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (30, 30)


class Ghost(Entity):
    count = 0
    fear_duration = 0
    eaten_ghosts = 0

    def __init__(self, img):
        super().__init__('Images/b' + img + "_up.png")
        Ghost.count += 1
        self.color = img
        self.rect.x = (11 + Ghost.count) * 20
        self.rect.y = 15 * 20
        self.vector = -1  # Направление
        self.dist = 0
        self.state = 'b'
        self.id = Ghost.count

    def back(self):
        self.rect.x = (11 + self.id) * 20
        self.rect.y = 15 * 20

    def change_direction(self):
        if Ghost.fear_duration > 0:
            self.state = 'd'
        else:
            self.state = 'b'
        temp = 'Images/' + self.state + self.color
        if self.vector == 0:
            temp += "_left.png"
        elif self.vector == 1:
            temp += "_up.png"
        elif self.vector == 2:
            temp += "_right.png"
        else:
            temp += "_down.png"

        self.image = pygame.image.load(temp).convert_alpha()
        self.save_image = self.image

    def update_vector(self, map, px, py):
        if Ghost.fear_duration > 0:
            Ghost.fear_duration -= 1
        else:
            Ghost.eaten_ghosts = 0
        x = self.rect.x // 20
        y = self.rect.y // 20
        coord = y * 28 + x
        is_valid1 = map.str_map[coord - 1] != '|' and map.str_map[coord - 1] != '*'
        is_valid2 = map.str_map[coord - 28] != '|' and map.str_map[coord - 28] != '*'
        is_valid3 = map.str_map[coord + 1] != '|' and map.str_map[coord + 1] != '*'
        is_valid4 = map.str_map[coord + 28] != '|' and map.str_map[coord + 28] != '*' and map.str_map[coord + 28] != ':'
        is_near = ((x - px) ** 2 + (y - py) ** 2) ** 0.5 <= 10.0 and self.rect.x % 20 == 0 and self.rect.y % 20 == 0
        if is_near and Ghost.fear_duration == 0:
            self.dist = 0
            if is_valid1 and x > px:
                self.vector = 0
            elif is_valid2 and y > py:
                self.vector = 1
            elif is_valid3 and x < px:
                self.vector = 2
            elif is_valid4 and y < py:
                self.vector = 3
            elif is_valid1 and x == px:
                self.vector = 0
            elif is_valid2 and y == py:
                self.vector = 1
            elif is_valid3 and x == px:
                self.vector = 2
            elif is_valid4 and y == py:
                self.vector = 3
            else:
                self.vector = -1
        elif is_near and Ghost.fear_duration > 0:
            self.dist = 0
            if is_valid3 and x > px:
                self.vector = 2
            elif is_valid4 and y > py:
                self.vector = 3
            elif is_valid1 and x < px:
                self.vector = 0
            elif is_valid2 and y < py:
                self.vector = 1
            elif is_valid3 and x == px:
                self.vector = 2
            elif is_valid4 and y == py:
                self.vector = 3
            elif is_valid1 and x == px:
                self.vector = 0
            elif is_valid2 and y == py:
                self.vector = 1
            else:
                self.vector = -1
        elif self.rect.x % 20 == 0 and self.rect.y % 20 == 0 and self.dist == 0:
            if (map.str_map[coord - 1] != '|' and map.str_map[coord - 1] != '*') and random.random() * 100 >= 25:
                self.vector = 0
            elif (map.str_map[coord - 28] != '|' and map.str_map[coord - 28] != '*') and random.random() * 100 >= 25:
                self.vector = 1
            elif (map.str_map[coord + 1] != '|' and map.str_map[coord + 1] != '*') and random.random() * 100 >= 25:
                self.vector = 2
            elif map.str_map[coord + 28] != '|' and map.str_map[coord + 28] != '*' and map.str_map[coord + 28] != ':':
                self.vector = 3
            else:
                self.vector = -1
        elif self.rect.x % 20 == 0 and self.rect.y % 20 == 0 and self.dist > 0:
            self.dist -= 1

        self.change_direction()

    def update(self, map, px, py):
        self.update_vector(map, px, py)

        if self.vector == 0:  # Left
            self.rect.x -= 1
        elif self.vector == 1:  # Up
            self.rect.y -= 1
        elif self.vector == 2:  # Right
            self.rect.x += 1
        elif self.vector == 3:  # Down
            self.rect.y += 1


class Heard(Entity):
    def __init__(self, img):
        super().__init__(img)


class Pacman(Entity):
    save_image = 0
    x = 0
    y = 0
    cord = 0
    color = 0
    score = 0
    image_count = 0
    image_rotate = ""

    def __init__(self, img):
        super().__init__(img)
        self.life = 3
        self.speed = 1

    def keyboard_cancel(self):
        self.key_a = False
        self.key_d = False
        self.key_s = False
        self.key_w = False

    def round_20(self, value):
        if value % 20 >= 10:
            value += 20 - value % 20
        else:
            value = value // 20 * 20

        return value

    def change_image(self):
        self.image = self.save_image
        self.image_count += 1

        if 0 < self.image_count < 20:
            self.image = pygame.image.load("pacman.png").convert_alpha()
        if 20 < self.image_count < 40:
            self.image = pygame.image.load("pacman1.png").convert_alpha()
        if 40 < self.image_count < 60:
            self.image = pygame.image.load("pacman2.png").convert_alpha()
        if self.image_count > 60:
            self.image_count = 0

        if self.image_rotate == 90:
            self.image = pygame.transform.rotate(self.image, 90)
        if self.image_rotate == 270:
            self.image = pygame.transform.rotate(self.image, 270)
        if self.image_rotate == "flip_left":
            self.image = pygame.transform.flip(self.image, 0, 0)
        if self.image_rotate == "flip_right":
            self.image = pygame.transform.flip(self.image, 90, 0)

    def keyboard_proccess(self, pressed_keys: set):
        if pygame.K_w in pressed_keys or pygame.K_s in pressed_keys or pygame.K_d in pressed_keys or pygame.K_a in pressed_keys:
            self.keyboard_cancel()
            self.image = self.save_image
            if pygame.K_w in pressed_keys:
                self.key_w = True
                self.image_rotate = 90
            elif pygame.K_s in pressed_keys:
                self.key_s = True
                self.image_rotate = 270
            elif pygame.K_d in pressed_keys:
                self.key_d = True
                self.image_rotate = "flip_left"
            elif pygame.K_a in pressed_keys:
                self.key_a = True
                self.image_rotate = "flip_right"
        if pygame.K_f in pressed_keys:
            self.keyboard_cancel()


    def update(self, map: TileMap, px, py):
        self.y = self.rect.y // 20
        self.x = self.rect.x // 20
        self.cord = ((self.y * 28) + self.x)
        if Ghost.fear_duration > 0:
            self.speed = 2
        else:
            self.speed = 1
        if map.str_map[self.cord] == '0':
            self.score += 10
            map.coins_count -= 1
            map.change_tile(self.cord, '.')
        if map.str_map[self.cord] == '@':
            Ghost.fear_duration = 1500
            map.change_tile(self.cord, '.')

        if self.key_w:
            self.rect.x = self.round_20(self.rect.x)

            # print(map.str_map[self.cord - 28], f"x: {self.cord % 28}, y: {self.cord // 28} rect.x: {self.rect.x} rect.y: {self.rect.y}")

            if (map.str_map[self.cord] == "." or map.str_map[self.cord] == '0' or map.str_map[
                self.cord] == '@') and self.rect.top > 20 and self.rect.x % 20 == 0:
                self.rect.y -= self.speed
            else:
                self.keyboard_cancel()

        if self.key_s:
            self.rect.x = self.round_20(self.rect.x)

            # print(map.str_map[self.cord + 28], f"x: {self.cord % 28}, y: {self.cord // 28} rect.x: {self.rect.x} rect.y: {self.rect.y}")

            if (map.str_map[self.cord + 28] == "." or map.str_map[self.cord + 28] == '0' or map.str_map[
                self.cord + 28] == '@') and self.rect.bottom < HEIGHT - 20 and self.rect.x % 20 == 0:
                self.rect.y += self.speed

        if self.key_a:
            if map.str_map[self.cord - 1] == "*":
                self.rect.x += 500
            else:
                self.rect.y = self.round_20(self.rect.y)

                # print(map.str_map[self.cord - 1], f"x: {self.cord % 28}, y: {self.cord // 28} rect.x: {self.rect.x} rect.y: {self.rect.y}")

                if (map.str_map[self.cord] == "." or map.str_map[self.cord] == '0' or map.str_map[
                    self.cord] == '@') and self.rect.left > 20 and self.rect.y % 20 == 0:
                    self.rect.x -= self.speed
                else:
                    self.keyboard_cancel()

        if self.key_d:
            # print(map.str_map[self.cord + 1], f"x: {self.cord % 28}, y: {self.cord // 28} rect.x: {self.rect.x} rect.y: {self.rect.y}")

            if map.str_map[self.cord + 1] == "*":
                self.rect.x -= 500
            else:
                self.rect.y = self.round_20(self.rect.y)
                if (map.str_map[self.cord + 1] == "." or map.str_map[self.cord + 1] == '0' or map.str_map[
                    self.cord + 1] == '@') and self.rect.right < WIDTH - 20 and self.rect.y % 20 == 0:
                    self.rect.x += self.speed
        self.change_image()

    def check_collision(self, screen, screen_width, screen_height, all_pacmans, heards):
        for pacman in all_pacmans:
            if round(pacman.rect.x, -1) == round(self.rect.x, -1) and round(pacman.rect.y, -1) == round(self.rect.y, -1):
                if Ghost.fear_duration > 0:
                    Ghost.eaten_ghosts += 1
                    self.score += 100 * 2 ** Ghost.eaten_ghosts
                elif self.life != 0:
                    self.life -= 1
                    heards.pop(self.life)
                    self.rect.x = 20
                    self.rect.y = 20
                if self.life <= 0:
                    # ВЫЗОВ МЕНЮ КОНЦА ИГРЫ СЮДЫ
                    file = "records.txt"
                    f = open(file, "r")
                    if int(f.read()) < self.score:
                        f = open(file, "w")
                        f.write(self.score.__str__())
                    f.close()
                    game_over = element.TextElement(text_getter=lambda: "GAME OVER", size=72,
                                                       font_name="Comic Sans MS",
                                                       color=(255, 0, 0))
                    game_over.draw_at(screen, screen_width, screen_height, 300, 250)

                    pygame.time.wait(4000)
                    return False
                pacman.back()
        return True
