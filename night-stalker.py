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
class Pixel:
    # To be used for all artwork
    def __init__(self, startX, startY, width = 2, height = 2):
        self.rect = pygame.Rect(startX, startY, width, height)

    def draw(self):
        pygame.draw.rect(SURFACE, ALL_LINES, self.rect)


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
        self.health = 100
        self.score = 0
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


    def update(self):
        KEYS = pygame.key.get_pressed()
        print(self.fire_timer)

        if self.current_state != HeroState.DEAD:
            if self.driving_mode[0].rect.y < 300:
                self.current_state = HeroState.FLYING
                self.dead_car = self.flying_mode
            else:
                self.current_state = HeroState.LANDED
                self.dead_car = self.driving_mode


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