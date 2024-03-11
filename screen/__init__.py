import pygame
import screen
import pygame.image
import element
import bindings
from TileMap import TileMap


class Screen(element.DrawableElement):
    def draw_at(self, screen, screen_width, screen_height, x: int, y: int, map, entities, px, py):
        pass

    def update(self, x: int, y: int, screen, map, entities, scores, px, py, pressed_keys: set):
        pass

class GameScreen(Screen):
    def __init__(self):
        self.pause_text = element.TextElement(text_getter=lambda: "Paused", size=120, color=(10, 10, 100))
        self.score_text = element.TextElement(text_getter=lambda: "Результат", size=40, color=(204, 119, 34))
        self.score = element.TextElement(text_getter=self.get_score, size=40, color=(204, 119, 34))
        self.best_score = element.TextElement(text_getter=lambda: "Лучший результат:", size=20)
        self.best_score_value = element.TextElement(text_getter=lambda: str(bindings.Bindings.best_score), size=20)
        self.score_int = 0
        self.paused = False

    def draw_at(self, screen, screen_width, screen_height, x: int, y: int, map, entities, px, py):
        """600 - размер игры, 20 - падинги"""
        if self.paused:
            self.pause_text.draw_at(screen, screen_width, screen_height, x + 250, y + 40)
        else:
            self.score_text.draw_at(screen, screen_width, screen_height, x + 600 + 10, y + 20)
            self.score.draw_at(screen, screen_width, screen_height, x + 600 + 10, y + 60)
            self.best_score.draw_at(screen, screen_width, screen_height, x + 600 + 10, y + 120)
            self.best_score_value.draw_at(screen, screen_width, screen_height, x + 600 + 10, y + 145)
            bindings.draw_world(screen, map, entities, px, py)

    def update(self, x: int, y: int, screen, map, entities, scores, px, py, pressed_keys):
        if pygame.K_p in pressed_keys:
            self.paused = not self.paused
        if self.paused:
            self.pause_text.update(x + 250, y + 40)
        else:
            pygame.draw.rect(screen, (0, 0, 0), (x + 650 + 20, y + 20, 30, 30))
            self.score_text.update(x + 600 + 10, y + 20)
            self.score.update(x + 600 + 10, y + 60)
            bindings.draw_world(screen, map, entities, px, py)
            self.best_score.update(x + 600 + 10, y + 120)
            self.best_score_value.update(x + 600 + 10, y + 145)
            self.score_int = scores

    def get_score(self):
        return self.score_int


def start_game(x, y, mx, my):
    """на параметры забейте - так надо"""
    bindings.Bindings.current_screen = screen.GameScreen()
    bindings.Bindings.game = True
    print("GameStarted")
    print(type(bindings.Bindings.current_screen))


class StatsScreen(Screen):
    def __init__(self):
        self.scores = list(bindings.Bindings.bests)
        self.scores.sort(reverse=True)
        while len(self.scores) > 30:
            self.scores.pop(len(self.scores) - 1)
        self.scores = list(map(str, self.scores))
        self.font = pygame.font.SysFont("Comic Sans MS", 18)

    def draw_at(self, screen, screen_width, screen_height, x: int, y: int, map, entities, px, py):
        screen.fill((57, 53, 52), (0, 0, 1000, 1000))
        (lw, lh) = self.font.size("Лучшие результаты")
        text_surface = self.font.render("Лучшие результаты", True, (0, 0, 0))
        self.font.size("Лучшие результаты")
        screen.blit(text_surface, (x + 400 - lw / 2, y + 10))
        padding = 36
        for i in self.scores:
            (sw, sh) = self.font.size(str(i))
            text_surface = self.font.render(str(i), True, (0, 0, 0))
            screen.blit(text_surface, (x + 400 - sw / 2, y + padding))
            padding += 24
        super().draw_at(screen, screen_width, screen_height, x, y, map, entities, px, py)

    def update(self, x: int, y: int, screenn, map, entities, scores, px, py, pressed_keys: set):
        super().update(x, y, screenn, map, entities, scores, px, py, pressed_keys)
        if pygame.K_ESCAPE in pressed_keys:
            bindings.Bindings.current_screen = screen.StartScreen()


def open_stats(x, y, mx, my):
    """на параметры забейте - так надо"""
    bindings.Bindings.current_screen = screen.StatsScreen()


def get_text():
    if TileMap.style == "spritesheet.png":
        return "Ретро"
    else:
        return "Modern"


def update_text(a, b, c, d):
    if TileMap.style == "spritesheet.png":
        TileMap.style = "spritesheet2.png"
    else:
        TileMap.style = "spritesheet.png"


class StartScreen(Screen):
    best_score_1 = 0

    def __init__(self):
        self.background = element.ImageElement(pygame.image.load("background.png"))
        self.score_int = 0
        self.game_start = element.AbstractButtonElement(action=start_game, width=522, height=59)
        self.exit = element.AbstractButtonElement(action=lambda x, y, mx, my: exit(0), width=253, height=59)
        self.stats = element.AbstractButtonElement(action=open_stats, width=253, height=59)
        self.style = element.TextButtonElement(action=update_text, text_element=element.TextElement(get_text, 43),
                                               width=522, height=60)

    def draw_at(self, screen, screen_width, screen_height, x: int, y: int, map, entities, px, py):
        self.background.draw_at(screen, screen_width, screen_height, x, y)
        self.style.draw_at(screen, screen_width, screen_height, x + 138, y + 525)
        super().draw_at(screen, 0, 0, x, y, map, entities, px, py)

    def update(self, x, y, screen, map, entities, scores, px, py, pressed_keys):
        self.game_start.update(x + 138, y + 393)
        self.style.update(x + 138, y + 525)
        self.exit.update(x + 141, y + 465)
        self.stats.update(x + 400, y + 462)
        self.background.update(x, y)
        super().update(0, 0, screen, map, entities, scores, px, py, pressed_keys)
        self.score_int = scores
        if pygame.K_s in pressed_keys:
            update_text(0, 0, 0, 0)

    def get_score(self):
        return self.score_int
