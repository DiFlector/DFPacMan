import screen


class Bindings:
    bests = set()
    best_score = 0
    """ЗАПРЕЩЕНО ТРОГАТЬ РУКАМИ. УБЬЕТ"""
    current_screen: screen.Screen = screen.StartScreen()
    """ЗАПРЕЩЕНО ТРОГАТЬ РУКАМИ. УБЬЕТ"""
    game = False

    @staticmethod
    def to_menu():
        Bindings.current_screen = screen.StartScreen()
        Bindings.game = False

def draw_world(screen, map, all_sprites, px, py):
    all_sprites.update(map, px, py)
    map.draw_map(screen)
    screen.blit(screen, (0, 0))
    all_sprites.draw(screen)
    pass


def update_world():
    pass


def update_best_score(score: int):
    """Должно вызываться в конце игры. Принимает результат."""
    global best_score
    best_score = max(score, best_score)
