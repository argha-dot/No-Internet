# THIS A CHROME OFFLINE DINO GAME RIPOFF MADE FOR PURELEY ENTERTAINMENT PURPOSES,
# ALL ASSETS ARE CREATED BY ME USING SUBLIME TEXT AND PAINT.NET.
# CURRENTLY, THERE IS NO DUCK FEATURE OR BIRDS, THE COLLISION IS SLIGHTLY OFF AND
# THE GAME LACKS A WORKING SCORING SYSTEM. ARIGATO.


import sys
import os
import time
import random
import pygame
import math
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

# ====================================================================================== #


# ====================================================================================== #
# GLOBAL VARIABLES


# GENERAL STUFF
win_wt, win_ht = 853, 480
fps_clock = pygame.time.Clock()
fps = 90

win = pygame.display.set_mode((win_wt, win_ht))
pygame.display.set_caption("NO INTERNET")
pygame.display.set_icon(load_img("ico.png"))

# IMAGES
cactus_1 = load_img("cactus_1.png").convert_alpha()
cactus_2 = load_img("cactus_2.png").convert_alpha()
cactus_3 = load_img("cactus_3.png").convert_alpha()

player_img = load_img("test.png").convert_alpha()
# ====================================================================================== #


# ====================================================================================== #
# PLAYER CLASS
class Player(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isJump = False
        self.img = player_img
        self.mask = pygame.mask.from_surface(self.img)

        self.max_jump = 11
        self.jump_offset = self.max_jump

    def draw(self, win):
        win.blit(self.img, (int(self.x), int(self.y)))

    def get_width(self):
        return self.img.get_rect().width

    def get_height(self):
        return self.img.get_rect().height

    # TO STIMUATE JUMPING, A QUADRATIC EQUATION IS USED.
    def do_jump(self, dt):
        keys = pygame.key.get_pressed()

        if not(self.isJump):
            self.check_bound()
            if keys[K_SPACE]:
                self.isJump = True

        else:
            if self.jump_offset >= -self.max_jump:
                dirn = 1
                if self.jump_offset < 0:
                    dirn *= -1
                if fps == 120:
                    dt = 0.01
                self.y -= (self.jump_offset**2) * 0.185 * dirn * dt * fps
                # print(dt)
                # print(round(dt, 2))
                self.jump_offset -= 1

            else:
                self.isJump = False
                self.jump_offset = self.max_jump

    # CHECKS IF THE PLAYER IS IN IT'S NEUTRAL POSITION, AND IF NOT, PUTS IT
    # THERE
    def check_bound(self):
        if self.y + self.img.get_rect().height - 10 != 389:
            self.y = 389 - self.img.get_rect().height + 10

# ====================================================================================== #


# ====================================================================================== #

# ENEMY CLASS
class Enemy(object):

    def __init__(self, x, y, speed, img):
        self.x = x
        self.y = y
        self.vel = speed
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move(self, dt):
        self.x -= int(self.vel * dt)

    def get_width(self):
        return self.img.get_rect().width

    def get_height(self):
        return self.img.get_rect().height

    def collide_mask(self, obj):
        return collide(self, obj)

    def collide_distance(self, obj):
        x, y = self.img.get_rect().center[0], self.img.get_rect().center[1]
        w, z = obj.img.get_rect().center[0], obj.img.get_rect().center[1]
        if math.hypot(x - w, y - z) >= (self.img.get_rect().center[0] + obj.img.get_rect().center[0]):
            print(math.hypot(x - w, y - z))
            print(self.img.get_rect().center[0] + obj.img.get_rect().center[0])
            return True
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
def collide(item, obj):
    offset_x = item.x - obj.x
    offset_y = item.y - obj.y
    return item.mask.overlap(obj.mask, (int(offset_x), int(offset_y))) != None
    pass
# ====================================================================================== #


# ====================================================================================== #
def main():
    pygame.init()
    level = 4

    # _________________________________________________________
    # STAR SCREEN
    def start_screen():
        font = pygame.font.Font(os.path.join("data", "font.ttf"), 70)
        title_font = font.render("No Internet", True, (200, 0, 0))


        def render_text(text, size=10):
            font_2 = pygame.font.Font(os.path.join("data", "font.ttf"), size)
            return font_2.render(text, True, (200, 0, 0))

        # OPTIONS
        start = [render_text("start", 20), [win_wt // 2 - render_text("start", 20).get_rect().width //
                                        2 + 10, 5 * win_ht // 8]]
        exit = [render_text("exit", 20),  [win_wt // 2 - render_text("exit", 20).get_rect().width //
                                                      2 + 10, 6 * win_ht // 8 - 20]]

        pos = [start, exit]
        cur = 0

        cursor = [load_img("cursor.png"), [start[1][0] - 25, start[1][1]]]
        

        logo = load_img("logo.png")
        player = Player(20, 389 - load_img("test.png").get_rect().height + 10)

        while True:
            bg = pygame.image.load(os.path.join(
                "data", "mountains.png")).convert()
            win.blit(bg, (0, 0))
            
            keys = pygame.key.get_pressed()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        terminate()

                    if (event.key == K_w or event.key == K_UP) and cur > 0:
                        cur -= 1
                    if (event.key == K_s or event.key == K_DOWN) and cur < len(pos) - 1 :
                        cur += 1
            
            if keys[K_SPACE] or keys[K_RETURN]:
                if cur == 0:
                    return  
                if cur == 1:
                    terminate()

            if keys[K_LALT]:
                return               
            
            cursor[1][0], cursor[1][1] = pos[cur][1][0] - 25, pos[cur][1][1]
            win.blit(cursor[0], cursor[1])


            win.blit(title_font, (win_wt // 2 - title_font.get_rect().width //
                                  2, win_ht // 5))

            win.blit(logo, (win_wt // 2 - logo.get_rect().width //
                            2, win_ht // 2 - logo.get_rect().height // 2 - 30))


            for position in pos:
                win.blit(position[0], position[1])

            player.draw(win)
            pygame.display.update()
            fps_clock.tick(fps)

    # _________________________________________________________
    # GAMEPLAY
    def run_game():
        skyx = 0
        groundx = 0
        vel = int(3)
        speed = vel * 120
        run = True

        # INITIALIZE THE ACTORS
        player = Player(20, 389 - player_img.get_rect().height + 10)
        enemies = []

        # MAIN GAME LOOP
        while run:

            player.draw(win)

            for enemy in enemies[:]:
                enemy.draw(win)

            pygame.display.update()

            out_events()
            dt = fps_clock.tick(fps) / 1000

            # DRAWS THE SKY AND MOVES IT
            sky_img = load_img("sky.png").convert()
            rel_sky = skyx % sky_img.get_rect().width
            win.blit(sky_img, (rel_sky - sky_img.get_rect().width, 0))
            skyx -= int(1 * dt + 1)

            if rel_sky < (win_wt):
                win.blit(sky_img, (rel_sky, 0))

            # DRAWS THE GROUND AND MOVES IT
            ground_img = load_img("ground.png").convert()
            rel_ground = groundx % ground_img.get_rect().width
            win.blit(ground_img, (rel_ground - ground_img.get_rect().width, 240))
            groundx -= int(speed * dt)

            if rel_ground < (win_wt):
                win.blit(ground_img, (rel_ground, 240))

            # CHOSES A RANDOM PLACE FOR THE ENEMY TO SPAWN
            xcoord = random.sample(
                range(win_wt + 50, win_wt + 800, 100), level)

            # GENERATES THE ENEMY LIST
            if len(enemies) < level:
                for i in xcoord:
                    enemy_img = random.choice([cactus_1, cactus_2, cactus_3])
                    enemy = Enemy(
                        i, 389 - enemy_img.get_rect().height + 10, speed, enemy_img)
                    enemies.append(enemy)

            # MAKES THE PLAYER JUMP
            player.do_jump(dt)

            # MOVES THE ENEMY
            for enemy in enemies[:]:
                enemy.move(dt)

                # COLLISION
                if (enemy.x + 4 <= player.x + player.get_width() and enemy.x + enemy.get_width() >=
                        player.x) and (enemy.y + 17 <= player.y + player.img.get_rect().height):
                    time.sleep(0.5)
                    return

            # REMOVES THE ENEMY IF IT GETS OUT OF THE SCREEN
            enemies[:] = [enemy for enemy in enemies if enemy.x +
                          enemy.img.get_rect().width > -5]

    # _________________________________________________________
    while True:
        start_screen()
        run_game()

# ====================================================================================== #

if __name__ == "__main__":
    main()
