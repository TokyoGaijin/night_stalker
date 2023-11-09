import pygame
from pygame import mixer
from enum import Enum
import random
import time
import sys
import pyautogui
import sqlite3

pygame.init() # for fonts and sounds

SCREEN = (800, 600)
SURFACE = pygame.display.set_mode(SCREEN)
BG = (0, 0, 0)
ALL_LINES = (255, 255, 255)

# Classes and Object Calls will go here
class GUI:
    # Management for score display and the life meter
    def __init__(self):
        self.life_rect = pygame.Rect(20, 60, 200, 30)

    def draw(self):
        pygame.draw.rect(SURFACE, ALL_LINES, self.life_rect)


class Pixel:
    # To be used for all artwork
    def __init__(self, startX, startY, width = 2, height = 2):
        self.rect = pygame.Rect(startX, startY, width, height)

    def draw(self):
        pygame.draw.rect(SURFACE, ALL_LINES, self.rect)


class BackState(Enum):
    CITY = 0
    MOUNTAINS = 1

class Background:
    def __init__(self):
        startX, startY = 800, 300 - 40
        self.back_images = [["--------------------------------------------------",
                             "--------------------------------------------------",
                             "--------------------------------------00----------",
                             "----------------------------00--------00----------",
                             "--------------------------00--00------00----------",
                             "-------------------------00----00-----00----------",
                             "------------------------00------00----00----------",
                             "---------------0000000000--0--0--00000000000------",
                             "---------------0-------00--0--0--00--------0------",
                             "---------------0-0--0--00--------00--0--0--0------",
                             "---------------0-0--0--00--0--0--00--0--0--0------",
                             "000000000------0-------00--------00--------0000000",
                             "0-------0------0-0--0--00--0--0--00--0--0--0-0-0-0",
                             "0-0-0-0-0------0-0--0--00--0--0--00--0--0--0-0-0-0",
                             "0-0-0-0-00000000-------00--------00--------0-----0",
                             "0-------0------0-0--0--00--0--0--00--0--0--0-0-0-0",
                             "0-0-0-0-0-0--0-0-0--0--00--0--0--00--0--0--0-0-0-0",
                             "0-0-0-0-0-0--0-0-------00--------00--------0-----0",
                             "0-------0------0-0--0--00--0--0--00--0--0--0-0-0-0",
                             "0-0-0-0-0-0--0-0-0--0--00--0--0--00--0--0--0-0-0-0"],

                            ["--------------------------------------------------",
                             "-----------------------o--------------------------",
                             "--------------0------00-00------0-----------------",
                             "------00-----0-0----0-----0---00-0----------------",
                             "-----0--0---0---0--0-------000----0----00---------",
                             "--- 0----0-0-----00---------0------00-0--0--------",
                             "---0------0------0-----------0-------0----0-------",
                             "--0--------0----0-------------0-----0------0--00--",
                             "-0----------0--0---------------0--0---------00--0-",
                             "0------------00-----------------0------------0---0",]]

        self.current_state = BackState.MOUNTAINS

        self.city_image = []
        self.mount_image = []

        def build_images():
            x, y = startX, startY
            for struct in self.back_images[0]:
                for col in struct:
                    if col == "0":
                        self.city_image.append(Pixel(x, y))
                    x += 2
                y += 2
                x = startX

            y = startY

            for rock in self.back_images[1]:
                for col in rock:
                    if col == "0":
                        self.mount_image.append(Pixel(x, y))
                    x += 2
                y += 2
                x = startX

        build_images()



class Bullet:
    def __init__(self, startX, startY):
        self.rect = pygame.Rect(startX, startY, 10, 2)
        self.SPEED = 8

    def update(self):
        self.rect.x += self.SPEED

    def draw(self):
        pygame.draw.rect(SURFACE, ALL_LINES, self.rect)



class HeroState(Enum):
    LANDED = 0
    FLYING = 1
    DEAD = 2

class NightStalker:
    # The Hero Class
    def __init__(self, startX, startY):
        self.SPEED = 5
        self.current_state = HeroState.LANDED
        self.score = 0

        self.hit_box = pygame.Rect(startX, startY, 50, 26)
        self.blueprint = [["00000--------------------",
                          "-0---0--------0000-------",
                          "--0---0------0----00-----",
                          "---0---0----0-------000--",
                          "----00000--0-----------00",
                          "-----0--0-0-------------0",
                          "--000------------------0^",
                          "---0--------------------0",
                          "--0---000-----------0000-",
                          "--0-00---00-------00---00",
                          "--000------00000000-----0",
                          "----00---00-------00---00",
                          "------000-----------000--"],

                          ["00000--------------------",
                          "-0---0--------0000-------",
                          "--0---0------0----00-----",
                          "---0---0----0-------000--",
                          "----00000--0-----------00",
                          "-----0--0-0-------------0",
                          "--000------------------0^",
                          "---0--------------------0",
                          "--0---000-----------0000-",
                          "--0-0000000-------0000000",
                          "--0000000000000000000000-"]]
        
        self.driving_mode = []
        self.flying_mode = []
        self.dead_car = self.driving_mode

        self.bullet_list = []
        self.fire_timer = 0
        self.COOLDOWN = 60

        self.display = GUI()

        def build_cars():
            x, y = startX, startY
            for row in self.blueprint[0]:
                for col in row:
                    if col == "0":
                        self.driving_mode.append(Pixel(x, y))
                    x += 2
                y += 2
                x = startX
            
            y = startY
            
            for row in self.blueprint[1]:
                for col in row:
                    if col == "0":
                        self.flying_mode.append(Pixel(x, y))
                    x += 2
                y += 2
                x = startX

        build_cars()


    
        

    def move(self, axis, speed):
        for pixel in self.driving_mode:
            if axis == "x":
                pixel.rect.x += speed
            if axis == "y":
                pixel.rect.y += speed

        for pixel in self.flying_mode:
            if axis == "x":
                pixel.rect.x += speed
            if axis == "y":
                pixel.rect.y += speed

        if axis == "x":
            self.hit_box.x += speed
        if axis == "y":
            self.hit_box.y += speed


    def get_hit(self):
        if self.current_state != HeroState.DEAD:
            self.display.life_rect.width -= 10
            if self.display.life_rect.width <= 0:
                self.display.life_rect.width = 0
    

    def draw(self):
        if self.current_state == HeroState.LANDED:
            for pixel in self.driving_mode:
                pixel.draw()
        elif self.current_state == HeroState.FLYING:
            for pixel in self.flying_mode:
                pixel.draw()
        else:
            for pixel in self.dead_car:
                pixel.draw()

        for bullet in self.bullet_list:
            bullet.draw()

        self.display.draw()


    def update(self):
        KEYS = pygame.key.get_pressed()
       
        if self.current_state != HeroState.DEAD:
            if self.driving_mode[0].rect.y < 300:
                self.current_state = HeroState.FLYING
                self.dead_car = self.flying_mode
            else:
                self.current_state = HeroState.LANDED
                self.dead_car = self.driving_mode

            if self.display.life_rect.width <= 0:
                self.current_state = HeroState.DEAD


        if self.current_state != HeroState.DEAD:
            if KEYS[pygame.K_a]:
                self.move("x", -self.SPEED)
            if KEYS[pygame.K_d]:
                self.move("x", self.SPEED)
            if KEYS[pygame.K_w]:
                self.move("y", -self.SPEED)
            if KEYS[pygame.K_s]:
                self.move("y", self.SPEED)
            if KEYS[pygame.K_SPACE]:
                if self.fire_timer == 0 and len(self.bullet_list) < 3:
                    self.bullet_list.append(Bullet(self.dead_car[37].rect.x - 5, self.dead_car[37].rect.y))
                    self.fire_timer += 1
            if not KEYS[pygame.K_SPACE]:
                self.fire_timer = 0

        if self.current_state == HeroState.DEAD:
            for pixel in self.dead_car:
                pixel.rect.x += random.randrange(-10, 11)
                pixel.rect.y += 8

        for bullet in self.bullet_list:
            bullet.update()
            if bullet.rect.x > 800:
                self.bullet_list.remove(bullet)












CLOCK = pygame.time.Clock()
FPS = 60
NAME = "Night Stalker™ by Michael Yamazaki-Fleisher ©2023-2024"

pygame.display.set_caption(NAME)

# Game subroutines go here
player = NightStalker(400, 300)




def die():
    confirm = pyautogui.confirm("Are you sure you want to exit to OS?", "Confirm", ["Yes", "No"])
    if confirm == "Yes":
        pygame.quit()
        sys.exit(1)

def draw():
    # Horizon Line
    pygame.draw.rect(SURFACE, ALL_LINES, pygame.Rect(0, 300, 800, 2))
    player.draw()

def update():
    CLOCK.tick(FPS)
    KEYS = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or KEYS[pygame.K_LCTRL] and KEYS[pygame.K_q]:
            die()

    draw()

    # Objects' update methods go here


    player.update()
    pygame.display.update()
    SURFACE.fill(BG)

def run():
    while True:
        update()

if __name__ == '__main__':
    run()