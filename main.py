import os.path
import pygame
from entity import Heard
import TileMap
from entity import Pacman
from entity import Ghost
from bindings import Bindings


display_width = 800
display_height = 620
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.init()
pygame.font.init()
pygame.display.set_caption('Pacman')
clock = pygame.time.Clock()

def new_game_init(score = 0, heartc = 3):
    map = TileMap.TileMap()
    all_sprites = pygame.sprite.Group()
    all_ghosts = pygame.sprite.Group()
    player = Pacman("pacman.png")
    player.score = score
    colors = ["blue", "orange", "pink", "red"]
    Ghost.count = 0
    all_sprites.add(player)

    for i in range(4):
        ghost = Ghost(colors[i])
        all_sprites.add(ghost)
        all_ghosts.add(ghost)

    hearts = []
    for i in range(heartc):
        hearts.append(Heard("heard.png"))
        hearts[i].rect.x = 620 + i * 30
        hearts[i].rect.y = 550

    return map, player, all_sprites, all_ghosts, hearts


def update_record():
    file = "records.txt"
    if os.path.exists(file):  # проверка что файл существует
        f = open(file, 'r')
        record = f.read()
        f.close()
        return record
    else:  # если файл не существует
        f = open(file, 'w')
        f.write("0")
        f.close()
        return 0


def update_hearts(hearts):
    for heart in hearts:
        gameDisplay.blit(heart.image, heart.rect)


def update_map(map : TileMap, player, ghosts):
    if map.coins_count == 0:
        player.rect.x = 20
        player.rect.y = 20

        for ghost in ghosts:
            ghost.back()

        return TileMap()

    return map


def play(record):
    is_alive = True
    map, player, all_sprites, all_ghosts, hearts = new_game_init()

    while is_alive:
        map = update_map(map, player, all_ghosts)
        pressed_keys = set()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pressed_keys.add(event.key)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        player.keyboard_proccess(pressed_keys)
        if len(pressed_keys) != 0:
            print(pressed_keys)
        gameDisplay.fill((0, 0, 0), (0, 0, 1000, 1000))
        Bindings.current_screen.update(0, 0, gameDisplay, map, all_sprites, player.score, player.x, player.y,
                                       pressed_keys)
        Bindings.current_screen.draw_at(gameDisplay, display_width, display_height, 0, 0, map, all_sprites, player.x,
                                        player.y)
        Bindings.current_screen.best_score_1 = record

        if Bindings.game:
            update_hearts(hearts)
            is_alive = player.check_collision(gameDisplay, display_width, display_height, all_ghosts, hearts)

        pygame.display.update()
        clock.tick(30)
    Bindings.bests.add(player.score)


def main():
    crashed = False
    while not crashed:
        record = update_record()
        bests = set()
        play(record)
        Bindings.to_menu()


if __name__ == "__main__":
    main()

pygame.quit()
quit()
