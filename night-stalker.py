import pygame
from pygame import mixer
from enum import Enum
import time
import sys
import pyautogui

pygame.init() # for fonts and sounds

SCREEN = (800, 600)
SURFACE = pygame.display.set_mode(SCREEN)
BG = (0, 0, 0)
ALL_LINES = (255, 255, 255)

# Classes and Object Calls will go here


CLOCK = pygame.time.Clock()
FPS = 60
NAME = "Night Stalker™ by Michael Yamazaki-Fleisher ©2023-2024"

pygame.display.set_caption(NAME)

# Game subroutines go here

def die():
    confirm = pyautogui.confirm("Are you sure you want to exit to OS?", "Confirm", ["Yes", "No"])
    if confirm == "Yes":
        pygame.quit()
        sys.exit(1)

def draw():
    pass

def update():
    CLOCK.tick(FPS)
    KEYS = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or KEYS[pygame.K_LCTRL] and KEYS[pygame.K_q]:
            die()

    draw()

    # Objects' update methods go here
    pygame.display.update()
    SURFACE.fill(BG)

def run():
    while True:
        update()

if __name__ == '__main__':
    run()