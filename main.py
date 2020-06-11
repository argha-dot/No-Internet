import os
import sys
import pygame
import random
import time
from pygame.locals import *


# SYNTHETIC SUGAR FOR CODE GRACEFUL CODE EXIT
def terminate():
    pygame.quit()
    sys.exit()


def check_for_key_press():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return key_up_events[0].key

# GAME EXIT


def out_events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            terminate()


def collide(item, obj):
    offset_x = item.x - obj.x
    offset_y = item.y - obj.y
    return item.mask.overlap(obj.mask, (int(offset_x), int(offset_y))) != None
    pass


# ENEMY CLASS
class Enemy(object):

    def __init__(self, x):
        self.x = x
        self.vel = speed
        self.hit = False
        self.img = random.choice(
            [load_img("cactus_1.png"), load_img("cactus_2.png")])
        self.mask = pygame.mask.from_surface(self.img)
        self.y = 389 - self.img.get_rect().height + 10

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    # MOVES THE ENEMY AT THE SAME SPEED AS THE GROUND, IN OPPOSITE DIRECTION TO GIVE THE  
    # ILLUSION OF THE ENEMY COMING TOWARDS THE PLAYER OR THE PLAYER RUNNING TOWARDS THE ENEMY

    def move(self):
        self.x -= self.vel

    def collide_mask(self, obj):
        return collide(self, obj)

    def collide_distance(self, obj):
        pass

    def collide_rect(self, obj):
        return (obj.img.get_rect().colliderect(self.img.get_rect())) 


# PLAYER CLASS
class Player(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isJump = False
        self.img = load_img("test.png")

        # SQUARE THIS NUMBER TO GET THE MAX JUMP HEIGHT IN PEXEL
        self.max_jump = 19
        self.jump_offset = self.max_jump
        self.mask = pygame.mask.from_surface(self.img)
        self.hit = False

    def draw(self, win):
        win.blit(self.img, (int(self.x), int(self.y)))
        pass 

    # MAKES THE PLAYER JUMP
    # TO STIMULATE GRAVITY LIKE JUMPIJNG, QUADRITIC EQUATION IS USED.
    def do_jump(self):
        keys = pygame.key.get_pressed()
        if self.isJump == False:
            if keys[K_SPACE]:
                self.isJump = True

        else:

            if self.jump_offset >= -self.max_jump:
                neg = 1

                if self.jump_offset < 0:
                    neg *= -1
                self.y -= (self.jump_offset**2) * 0.05 * neg
                self.jump_offset -= 1

            else:
                self.isJump = False
                self.jump_offset = self.max_jump


class sprite(object):

    def __init__(self, filename, cols, rows):
        self.sheet = load_img(filename)

        self.cols = cols
        self.rows = rows
        self.cell_cnt = cols * rows

        self.rect = self.sheet.get_rect()
        w = self.cell_w = self.rect.width / cols
        h = self.cell_h = self.rect.height / rows

        self.cells = list([int(i % cols * w), int(i // cols * h), w, h]
                          for i in range(self.cell_cnt))

    def draw(self, win, cell_index, x, y):
        win.blit(self.sheet, (x, y), self.cells[cell_index])


# SYNTHETIC SYGAR, LOADS AN IMAGE, AND CONVERTS THE ALPHA
def load_img(name):
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as e:
        print("Can't load image: ", name)
        raise SystemExit(e)
    image = image.convert_alpha()
    return image

# START SCREEN
def start_screen():
    font = pygame.font.Font(os.path.join("data", "font.ttf"), 70)
    title_font = font.render("No Internet", True, (200, 0, 0))

    font_2 = pygame.font.Font(os.path.join("data", "font.ttf"), 30)
    title_ = font_2.render("Press Space to Jump", True, (200, 0, 0))
    logo = load_img("logo.png")

    player = Player(20, 389 - load_img("test.png").get_rect().height + 10)

    while True:
        bg = pygame.image.load(os.path.join("data", "mountains.png")).convert()
        display_surf.blit(bg, (0, 0))
        if check_for_key_press():
            pygame.event.get()
            return

        display_surf.blit(title_font, (win_wt // 2 - title_font.get_rect().width //
                                       2, win_ht // 5))

        display_surf.blit(logo, (win_wt // 2 - logo.get_rect().width //
                                 2, win_ht // 2 - logo.get_rect().height // 2))

        display_surf.blit(title_, (win_wt // 2 - title_.get_rect().width //
                                       2, 7 * win_ht // 8))

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

        player.draw(display_surf)
        pygame.display.update()
        fps_clock.tick(fps)


# MAIN FUNCTION
def main():
    global win_wt, win_ht, speed, display_surf, fps, fps_clock

    # VARIABLES
    win_wt, win_ht = 853, 480
    fps = 120
    speed = 2

    # SETS THE LOCATION OF THE WINDOW

    # INITAILISES THE DISPLAY WINDOW
    display_surf = pygame.display.set_mode((win_wt, win_ht))
    pygame.init()

    # TO LIMIT THE FPS
    fps_clock = pygame.time.Clock()

    # GAMEPLAY LOOP
    def run_game():
        global index, x, x_2
        index = 0
        x = 0
        x_2 = 0

        # THE NUMBER OF ENEMIES ON THE SCREEN AT A TIME
        level = 4

        # INITIZATION OF THE CHARACTERS
        player = Player(20, 389 - load_img("test.png").get_rect().height + 10)
        enemies = []

        # REDRAWS THE GAME WINDOW, THIS IS WHAT HAPPENS EVERY 1 BY FPS'TH
        # SECOND OF THE GAME
        def redraw_game_win():
            global index, x, x_2

            display_surf.fill((0, 0, 0))

            # GROUND MOVEMENT
            bg_img = pygame.image.load(
                os.path.join("data", "ground.png")).convert()
            rel_x = x % bg_img.get_rect().width
            display_surf.blit(bg_img, (rel_x - bg_img.get_rect().width, 240))
            x -= speed
            if rel_x < (win_wt):
                display_surf.blit(bg_img, (rel_x, 240))

            # SKY MOVEMENT
            bg_img_2 = pygame.image.load(
                os.path.join("data", "sky.png")).convert()
            rel_x_2 = x_2 % bg_img_2.get_rect().width
            display_surf.blit(
                bg_img_2, (rel_x_2 - bg_img_2.get_rect().width, 0))
            x_2 -= 1

            if rel_x_2 < (win_wt):
                display_surf.blit(bg_img_2, (rel_x_2, 0))

            # s.draw(display_surf, index % s.cell_cnt, 20, 389 - 39)
            # index += 1

            # PLAYER
            player.draw(display_surf)

            # ENEMEY
            for enemy in enemies[:]:
                enemy.draw(display_surf)

            # UPDATES THE DISPLAY
            pygame.display.update()

        # MAIN GAME LOOP. FUNNY IT IS THE SMALLEST BLOCK OF CODE IN ALL THIS.
        while True:
            redraw_game_win()
            player.do_jump()

            out_events()

            if len(enemies) < level:
                for i in range(level):
                    enemy = Enemy(random.randrange(
                        win_wt + 50, win_wt + 1050, 100))
                    enemies.append(enemy)

            for enemy in enemies[:]:
                enemy.move()
                if enemy.img.get_rect().colliderect(player.img.get_rect()):
                    print("q")
                    # time.sleep(0.5)
                    # return

            enemies[:] = [enemy for enemy in enemies if enemy.x +
                          enemy.img.get_rect().width > -5]

            fps_clock.tick(fps)

    while True:
        start_screen()

        run_game()


if __name__ == "__main__":
    main()
