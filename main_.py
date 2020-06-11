import sys
import os
import time
import random
import pygame
from pygame.locals import *

# ====================================================================================== #
# SYNTHETIC SUGARS


# FOR GRACEFUL EXITS
def terminate():
    pygame.quit()
    sys.exit()


# FOR EXIT OUT OF THE GAME LOOP
def out_events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            terminate()


# PATHNAME
def fullname(name):
    return os.path.join("data", name)


# LOAD IMAGE
def load_img(name):
    try:
        image = pygame.image.load(fullname(name))
    except pygame.error as e:
        print("Can't load image:", name)
        raise SystemExit(e)
    return image


# CHECKS FOR KEY PRESSES
def check_for_key_press():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return key_up_events[0].key
# ====================================================================================== #


# ====================================================================================== #
# GLOBAL VARIABLES


# GENERAL STUFF
win_wt, win_ht = 853, 480
fps_clock = pygame.time.Clock()
fps = 60

win = pygame.display.set_mode((win_wt, win_ht))
pygame.display.set_caption("NO INTERNET")
pygame.display.set_icon(load_img("ico.png"))

# IMAGES
cactus_1 = load_img("cactus_1.png").convert_alpha()
cactus_2 = load_img("cactus_2.png").convert_alpha()
enemy_img = random.choice([cactus_1, cactus_2])

player_img = load_img("test.png").convert_alpha()
# ====================================================================================== #


# ====================================================================================== #
class Player(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isJump = False
        self.img = player_img

        self.max_jump = 12
        self.jump_offset = self.max_jump

    def draw(self, win):
        win.blit(self.img, (int(self.x), int(self.y)))

    def do_jump(self):
        keys = pygame.key.get_pressed()

        if self.isJump == False:
            if keys[K_SPACE]:
                self.isJump = True

        else:
            if self.jump_offset >= -self.max_jump:
                dirn = 1
                if self.jump_offset < 0:
                    dirn *= -1
                self.y -= (self.jump_offset**2) * 0.2 * dirn
                self.jump_offset -= 1

            else:
                self.isJump = False
                self.jump_offset = self.max_jump
# ====================================================================================== #


# ====================================================================================== #
class Enemy(object):

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.vel = speed
        self.img = enemy_img

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move(self):
        self.x -= self.vel
# ====================================================================================== #


# ====================================================================================== #
class Sprite(object):

    def __init__(self, filename, cols, rows):
        self.sheet = load_img(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.cell_cnt = rows * cols

        self.rect = self.sheet.get_rect()
        w = self.cell_w = self.rect.width / cols
        h = self.cell_h = self.rect.height / rows

        self.cells = list([int(i % cols * w), int(i // cols * h), w, h]
                          for i in range(self.cell_cnt))

    def draw(self, win, cell_index, x, y):
        win.blit(self.sheet, (x, y), self.cells[cell_index])
# ====================================================================================== #


# ====================================================================================== #
def main():
    pygame.init()
    speed = 3
    level = 3
    os.environ["SDL_VIDEO_WINDOW_POS"] = "0, 0"
    player = Player(20, 389 - player_img.get_rect().height + 10)
    enemies = []
    # enemy = Enemy(600, 389 - enemy_img.get_rect().height + 10, speed)

    # _________________________________________________________
    def redraw_game_win():
        player.draw(win)

        for enemy in enemies[:]:
            enemy.draw(win)
        
        pygame.display.update()


    # _________________________________________________________
    def start_screen():
        font = pygame.font.Font(os.path.join("data", "font.ttf"), 70)
        title_font = font.render("No Internet", True, (200, 0, 0))

        font_2 = pygame.font.Font(os.path.join("data", "font.ttf"), 30)
        title_ = font_2.render("Press Space to Jump", True, (200, 0, 0))
        logo = load_img("logo.png")

        player = Player(20, 389 - load_img("test.png").get_rect().height + 10)

        while True:
            bg = pygame.image.load(os.path.join("data", "mountains.png")).convert()
            win.blit(bg, (0, 0))
            if check_for_key_press():
                pygame.event.get()
                return

            win.blit(title_font, (win_wt // 2 - title_font.get_rect().width //
                                           2, win_ht // 5))

            win.blit(logo, (win_wt // 2 - logo.get_rect().width //
                                     2, win_ht // 2 - logo.get_rect().height // 2))

            win.blit(title_, (win_wt // 2 - title_.get_rect().width //
                                           2, 7 * win_ht // 8))

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()

            player.draw(win)
            pygame.display.update()
            fps_clock.tick(fps)


    # _________________________________________________________
    def run_game():
        skyx = 0
        groundx = 0
        
        while True:
            win.fill((0, 0, 0))

            sky_img = load_img("sky.png").convert()
            rel_sky = skyx % sky_img.get_rect().width
            win.blit(sky_img, (rel_sky - sky_img.get_rect().width, 0))
            skyx -= 1

            if rel_sky < (win_wt):
                win.blit(sky_img, (rel_sky, 0))

            ground_img = load_img("ground.png").convert()
            rel_ground = groundx % ground_img.get_rect().width
            win.blit(ground_img, (rel_ground - ground_img.get_rect().width, 240))
            groundx -= speed

            if rel_ground < (win_wt):
                win.blit(ground_img, (rel_ground, 240))

            xcoord = random.sample(range(win_wt + 50, win_wt + 750, 70), level)

            if len(enemies) < level:
                for i in xcoord:
                    enemy = Enemy(i, 389 - enemy_img.get_rect().height + 10, speed)
                    enemies.append(enemy)

            player.do_jump()
            
            for enemy in enemies[:]:
                enemy.move()

            enemies[:] = [enemy for enemy in enemies if enemy.x +
                          enemy.img.get_rect().width > -5]

            redraw_game_win()
            out_events()

            fps_clock.tick(fps)

# _________________________________________________________

    while True:
        start_screen()
        run_game()
# ====================================================================================== #

if __name__ == "__main__":
    main()
