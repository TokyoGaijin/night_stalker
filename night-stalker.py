import pygame
from pygame import mixer
from enum import Enum
import random
import sys
import pyautogui
import sqlite3

pygame.init() # for fonts and sounds


SCREEN = (800, 600)
SURFACE = pygame.display.set_mode(SCREEN)
BG = (0, 0, 0)
ALL_LINES = (255, 255, 255)


class Scoreboard:
    def __init__(self):
        self.conn = sqlite3.connect('masterbase.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS HighScores(NAME text, SCORE int)")
        self.scores = []
        self.pen = Writer(font="consola.ttf", size=20)
        self.game_pen = Writer()
        
    def submit(self, name, score):
        self.c.execute(f'INSERT INTO HighScores(NAME, SCORE) VALUES ("{name}", {score})')
        self.conn.commit()
        
    def reset(self):
        self.submit("Michael", 19000)
        self.submit("Nakaya", 18000)
        self.submit("Sabato", 17000)
        self.submit("Gaia", 16000)
        self.submit("Tateishi", 15000)
        self.submit("Imai", 14000)
        self.submit("Sakita", 13000)
        self.submit("Allan", 12000)
        self.submit("Sakita", 11000)
        self.submit("Jackson", 10000)
        self.submit("Shiwa", 9000)
        
    def register(self, score):
        user_name = pyautogui.prompt("Please enter your name.")
        self.submit(user_name, score)
        
    def draw(self):
        score_list = []
        self.scores = self.c.execute("SELECT NAME, SCORE FROM HighScores ORDER BY SCORE DESC LIMIT 10").fetchall()
        for i in range(len(self.scores)):
            rank = i + 1
            score_list.append(f"{rank}: {self.scores[i][0]} {self.scores[i][1]}")
        
        self.game_pen.write("PRESS ENTER", (300, 550))
        self.game_pen.write("HIGH SCORES", (280, 260))
        for i, score in enumerate(score_list):
            self.pen.write(score, (300, 300 + i * 20))
        
        
class Title:
    def __init__(self, startX, startY):
        self.blueprint = ["00-----0----00-----000000-----00---00----00000000---------------------------------------------------",
                          "000----0----00----00-----0----00---00-------00------------------------------------------------------",
                          "0-00---0----00----00----------00---00-------00------------------------------------------------------",
                          "0--00--0----00----00--0000----0000000-------00------------------------------------------------------",
                          "0---00-0----00----00----00----00---00-------00------------------------------------------------------",
                          "0----000----00----00----00----00---00-------00------------------------------------------------------",
                          "0-----00----00-----000000-----00---00-------00------------------------------------------------------",
                          "----------------------------------------------------------------------------------------------------",
                          "----------------------000000-----00000000-----00000-----00---------00---00----0000000----0000000----",
                          "--------------------00------0-------00-------00---00----00---------00--00-----00---------00----00---",
                          "--------------------000-------------00-------00---00----00---------00-00------00---------00-----00--",
                          "-----------------------000----------00-------0000000----00---------0000-------00000------00-----00--",
                          "------------------------000---------00-------00---00----00---------0000-------00---------00000000---",
                          "-------------------------000--------00-------00---00----00---------00-00------00---------00-----00--",
                          "--------------------00-----00-------00-------00---00----00---------00--00-----00---------00-----00--",
                          "----------------------00000---------00-------00---00----0000000----00---00----0000000----00-----00--",
                          "----------------------------------------------------------------------------------------------------",
                          "000-0-0--000------0--00---00--0--00--000------0---00--000-0--0--0--0------00-0-0--0---0--000-000-00-",
                          "-0--0-0--0-------0-0-0-0-0---0-0-0-0-0-------0-0-0-----0--0-0-0-00-0-----0---0-0-0-0-0-0--0--0---0-0",
                          "-0--000--00------000-000-0---000-0-0-00------000-0-----0--0-0-0-0-00------0--000-0-0-0-0--0--00--000",
                          "-0--0-0--000-----0-0-0-0--00-0-0-00--000-----0-0--00---0--0--0--0--0-----000-0-0--0---0---0--000-0-0",]
        
        self.title_list = []
        def build():
            x, y = startX, startY
            for row in self.blueprint:
                for col in row:
                    if col == "0":
                        self.title_list.append(Pixel(x, y, width = 5, height = 5))
                    x += 5
                y += 5
                x = startX
        build()
        
    def draw(self):
        for pixel in self.title_list:
            pixel.draw()


# TODO: High Scores DB 
# TODO: Title Screen with high score display
# TODO: BGM (?)

class Soundboard:
    def __init__(self):
        self.explosion = pygame.mixer.Sound("boom.wav")
        self.hit = pygame.mixer.Sound("hit.wav")
        self.victim_dies = pygame.mixer.Sound("victim_killed.wav")
        self.fire = pygame.mixer.Sound("laser.mp3")
        self.rescue = pygame.mixer.Sound("rescue.mp3")

    def play(self, sound):
        sound.play()

class GameState(Enum):
    TITLE = 0 # Title Screen
    MAIN = 1 # Main Gameplay
    TRANSITION = 2 # Transition of levels
    GAME_OVER = 3 # Self Explanatory


class Writer:
    def __init__(self, font = "ARCADECLASSIC.TTF", size = 40):
        self.SIZE = size
        self.FONT = pygame.font.Font(font, self.SIZE)
        
    def write(self, string_to_write, coords):
        showtext = self.FONT.render(string_to_write, self.SIZE, ALL_LINES)
        SURFACE.blit(showtext, coords)

class GUI:
    # Management for score display and the life meter
    def __init__(self):
        self.pen = Writer()
        self.life_rect = pygame.Rect(20, 60, 200, 30)

    def draw(self):
        pen.write("LIFE", (20, 18))
        pygame.draw.rect(SURFACE, ALL_LINES, self.life_rect)


class TitleScreen:
    def __init__(self):
        pass


class Pixel:
    # To be used for all artwork
    def __init__(self, startX, startY, width = 2, height = 2):
        self.rect = pygame.Rect(startX, startY, width, height)

    def draw(self):
        pygame.draw.rect(SURFACE, ALL_LINES, self.rect)


class Pow:
    def __init__(self, startX, startY):
        self.hitbox = pygame.Rect(startX, startY, 20, 20)
        self.pow = []
        self.blueprint = ["--000000--",
                          "-00--0000-",
                          "000--00000",
                          "000--00000",
                          "000--00000",
                          "000--00000",
                          "000--00000",
                          "000-----00",
                          "-00000000-",
                          "--000000--"]
        
        self.SPEED = 6
        def build_pow():
            x, y = startX, startY
            for row in self.blueprint:
                for col in row:
                    if col == "0":
                        self.pow.append(Pixel(x, y))
                    x += 2

                y += 2
                x = startX
        
        build_pow()

    def draw(self):
        for pixel in self.pow:
            pixel.draw()

    def update(self):
        for pixel in self.pow:
            pixel.rect.x -= self.SPEED
        self.hitbox.x -= self.SPEED

class BackState(Enum):
    CITY = 0
    MOUNTAINS = 1

class Background:
    def __init__(self, startX = 800, startY = 300 - 40, state = BackState.MOUNTAINS):
        self.startX, self.startY = startX, startY
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
                             "--------------------------------------------------",
                             "--------------------------------------------------",
                             "--------------------------------------------------",
                             "--------------------------------------------------",
                             "--------------------------------------------------",
                             "--------------------------------------------------",
                             "--------------------------------------------------",
                             "--------------------------------------------------",
                             "--------------------------------------------------",
                             "--------------------------------------------------",
                             "-----------------------o--------------------------",
                             "--------------0------00-00------0-----------------",
                             "------00-----0-0----0-----0---00-0----------------",
                             "-----0--0---0---0--0-------000----0----00---------",
                             "--- 0----0-0-----00---------0------00-0--0--------",
                             "---0------0------0-----------0-------0----0-------",
                             "--0--------0----0-------------0-----0------0--00--",
                             "-0----------0--0---------------0--0---------00--0-",
                             "0------------00-----------------0------------0---0",]]

        self.current_state = state

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

    def draw(self):
        if self.current_state == BackState.MOUNTAINS:
            for i in self.mount_image:
                i.draw()
        if self.current_state == BackState.CITY:
            for i in self.city_image:
                i.draw()

    def update(self):
        if self.current_state == BackState.MOUNTAINS:
            for pixel in self.mount_image:
                pixel.rect.x -= 3
        if self.current_state == BackState.CITY:
            for pixel in self.city_image:
                pixel.rect.x -= 3
                    
class Star:
    def __init__(self, startX, startY):
        self.rect = Pixel(startX, startY)
    
    def draw(self):
        self.rect.draw()
        
    def update(self):
        self.rect.rect.x -= 1
        if self.rect.rect.x <= 3:
            self.rect.rect.x = 800
            self.rect.rect.y = random.randint(40, 150)        


class Bullet:
    def __init__(self, startX, startY, vertical = False):
        self.rect = pygame.Rect(startX, startY, 10, 2)
        self.vertical = vertical
        self.SPEED = 6

    def update(self):
        if self.vertical:
            self.rect.y -= self.SPEED # Speed is being overridden somewhere so the signs must be flipped
        else:
            self.rect.x += self.SPEED


    def draw(self):
        pygame.draw.rect(SURFACE, ALL_LINES, self.rect)


class EnemyState(Enum):
    ALIVE = 0
    DEAD = 1

class EnemyType(Enum):
    BIKE = 0
    PLANE = 1

class Enemy:
    def __init__(self, startX, enemy_type):
        if enemy_type == EnemyType.BIKE:
            startY = random.randint(350, 424)
        if enemy_type == EnemyType.PLANE:
            startY = random.randint(50, 274)
        self.speed = random.randint(3, 6)
        self.direction = ["left", "right"]
        self.hitbox = pygame.Rect(startX, startY, 50, 26)
        self.blueprint = [["-------------------------",
                           "--------000--------------",
                           "--------00000------------",
                           "000------0000------------",
                           "--0000000000-------------",
                           "---00000000---0000000000-",
                           "---0----000---0000000----",
                           "----0---000---0000000----",
                           "----00000000000----------",
                           "----0000000000000000-----",
                           "---00---------------00---",
                           "-00--00-----------00--00-",
                           "---00---------------00---",],

                          ["-------------------000000",
                           "-------------------00000^",
                           "-----------------000000--",
                           "---------------0000000---",
                           "--------0000000000000----",
                           "-----0---0000000000000---",
                           "--000000000000000000000--",
                           "----000000000000000000---",
                           "-------0000000000000000--",
                           "----------00000000000----",
                           "------------0000000000---",
                           "---------------00000000--",
                           "-------------00000000000-",]]
        self.current_state = EnemyState.ALIVE
        self.bike = []
        self.plane = []
        self.bullet_list = []
        self.fire_timer = 0
        self.COOLDOWN = 60
        self.points = 47
        
        def build_bad_guys():
            x, y = startX, startY
            for row in self.blueprint[0]:
                for col in row:
                    if col == "0":
                        self.bike.append(Pixel(x, y))
                    x += 2
                y += 2
                x = startX

            y = startY

            for row in self.blueprint[1]:
                for col in row:
                    if col == "0":
                        self.plane.append(Pixel(x, y))
                    x += 2
                y += 2
                x = startX

        build_bad_guys()
        self.enemy_type = enemy_type

    def draw(self):
        if self.enemy_type == EnemyType.BIKE:
            for pixel in self.bike:
                pixel.draw()
        if self.enemy_type == EnemyType.PLANE:
            for pixel in self.plane:
                pixel.draw()
        for bullet in self.bullet_list:
            bullet.draw()

    def update(self):
        self.fire_timer += 1
        if self.current_state == EnemyState.ALIVE:
            if self.fire_timer % self.COOLDOWN == 0:
                if self.enemy_type == EnemyType.BIKE:
                    self.bullet_list.append(Bullet(self.hitbox.x, self.hitbox.y + 8))
                if self.enemy_type == EnemyType.PLANE:
                    self.bullet_list.append(Bullet(self.hitbox.x + 26, self.hitbox.y + 24, vertical = random.choice([True, False])))
        
            for bullet in self.bullet_list:
                bullet.update()
                bullet.SPEED = -8 # to go the other way
                if bullet.rect.right < 0 or bullet.rect.top > 450:
                    self.bullet_list.remove(bullet)

            if self.enemy_type == EnemyType.BIKE:
                for pixel in self.bike:
                    pixel.rect.x -= self.speed
            if self.enemy_type == EnemyType.PLANE:
                for pixel in self.plane:
                    pixel.rect.x -= self.speed

            self.hitbox.x -= self.speed

        if self.current_state == EnemyState.DEAD:
            if self.enemy_type == EnemyType.BIKE:
                for pixel in self.bike:
                    pixel.rect.x += random.randint(4, 10)
            if self.enemy_type == EnemyType.PLANE:
                for pixel in self.plane:
                    pixel.rect.x += random.randint(4, 10)
            self.hitbox.x = 9000



class HeroState(Enum):
    LANDED = 0
    FLYING = 1
    DEAD = 2

class NightStalker:
    # The Hero Class
    def __init__(self, startX, startY, score = 0):
        self.speed = 5
        self.current_state = HeroState.LANDED
        self.score = score
        self.pen = Writer()
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
        self.victims_saved = 0
        self.bullet_list = []
        self.fire_timer = 0
        self.COOLDOWN = 60
        self.MAX_LIFE = 200
        self.kill_count = 0
        self.soundman = Soundboard()
        

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


    def get_hit(self, damage = 0):
        if self.current_state != HeroState.DEAD:
            self.display.life_rect.width -= 10 + damage
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
            if self.driving_mode[0].rect.y < 350:
                self.current_state = HeroState.FLYING
                self.dead_car = self.flying_mode
            else:
                self.current_state = HeroState.LANDED
                self.dead_car = self.driving_mode

            if self.display.life_rect.width <= 0:
                self.current_state = HeroState.DEAD


        if self.current_state != HeroState.DEAD:
            if KEYS[pygame.K_a]:
                self.move("x", -self.speed)
            if KEYS[pygame.K_d]:
                self.move("x", self.speed)
            if KEYS[pygame.K_w]:
                self.move("y", -self.speed)
            if KEYS[pygame.K_s]:
                self.move("y", self.speed)
            if KEYS[pygame.K_SPACE]:
                if self.fire_timer == 0 and len(self.bullet_list) < 3:
                    self.soundman.play(self.soundman.fire)
                    self.bullet_list.append(Bullet(self.dead_car[37].rect.x - 5, self.dead_car[37].rect.y))
                    self.fire_timer += 1
            if not KEYS[pygame.K_SPACE]:
                self.fire_timer = 0

        if self.current_state == HeroState.DEAD:
            for pixel in self.dead_car:
                pixel.rect.x += random.randrange(-10, 11)
                pixel.rect.y += 8
            self.hit_box.x = 9000

        for bullet in self.bullet_list:
            bullet.update()
            if bullet.rect.x > 800:
                self.bullet_list.remove(bullet)
                
        if self.dead_car[-1].rect.bottom >= 450 and KEYS[pygame.K_s]:
            self.speed = 0
        else:
            self.speed = 5
            
        if self.dead_car[-1].rect.bottom > 454:
            self.current_state = HeroState.DEAD
            
        pen.write(f"SCORE    {self.score}", (400,18))

class Victim:
    def __init__(self, startX, startY):
        self.hit_box = pygame.Rect(startX, startY, 20, 20)
        self.image = ["0---00---0",
                      "-0-0000-0-",
                      "--0-00-0--",
                      "---0000---",
                      "----00----",
                      "----00----",
                      "---0--0---",
                      "--0----0--",
                      "--0----0--",
                      "000----000"]
        self.victim = []
        def make_victim():
            x, y = startX, startY
            for row in self.image:
                for bodypart in row:
                    if bodypart == "0":
                        self.victim.append(Pixel(x, y))
                    x += 2
                y += 2
                x = startX
        make_victim()
        
    def draw(self):
        for part in self.victim:
            part.draw()
            
    def update(self):
        for part in self.victim:
            part.rect.x -= 4
        self.hit_box.x -= 4
        



CLOCK = pygame.time.Clock()
FPS = 60
NAME = "Night Stalker™ by Michael Yamazaki-Fleisher ©2023-2024"

pygame.display.set_caption(NAME)
pygame.mouse.set_visible(False)

# Game subroutines go here
player = NightStalker(400, 300)
pen = Writer()
bg_list = []
victim_list = []
enemy_list = []
starfield = [Star(random.randint(0, 798), random.randint(40, 150)) for i in range(30)]
roadlines_list = [pygame.Rect(0, 400, 200, 2), pygame.Rect(400, 400, 200, 2), pygame.Rect(800, 400, 200, 2)]
POW_list = []
SOUNDBOARD = Soundboard()
current_gameState = GameState.TITLE
max_enemies = 3
clear_count = 30
scoreboard = Scoreboard()
title = Title(150, 50)


def game_init(next_level = True):
    global player, victim_list, enemy_list, POW_list, max_enemies, clear_count, current_gameState
    victim_list, enemy_list, POW_list = [], [], []
    if next_level:
        new_score = player.score
        player = NightStalker(400, 300, new_score)
        max_enemies += 2
        clear_count += 10
    else:
        player.score = 0
        max_enemies = 3
        player.kill_count = 0
        clear_count = 30
        player.victims_saved = 0
        player = NightStalker(400, 300)
    player.kill_count = 0
        

    
    current_gameState = GameState.MAIN


def die():
    confirm = pyautogui.confirm("Are you sure you want to exit to OS?", "Confirm", ["Yes", "No"])
    if confirm == "Yes":
        pygame.quit()
        sys.exit(1)

def draw():
    if current_gameState == GameState.MAIN:
        for bgs in bg_list:
            bgs.draw()
        for star in starfield:
            star.draw()
        # Horizon Line
        pygame.draw.rect(SURFACE, ALL_LINES, pygame.Rect(0, 300, 800, 2))
        # Road lanes
        pygame.draw.rect(SURFACE, ALL_LINES, pygame.Rect(0, 350, 800, 2))
        pygame.draw.rect(SURFACE, ALL_LINES, pygame.Rect(0, 450, 800, 2))
        for lines in roadlines_list:
            pygame.draw.rect(SURFACE, ALL_LINES, lines)
        for victim in victim_list:
            victim.draw()

        for enemy in enemy_list:
            enemy.draw()

        for pow in POW_list:
            pow.draw()
            
        player.draw()


    if current_gameState == GameState.TITLE:
        scoreboard.draw()
        title.draw()

def update():
    global current_gameState
    CLOCK.tick(FPS)
    KEYS = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or KEYS[pygame.K_LCTRL] and KEYS[pygame.K_q]:
            die()
    
    draw()

    if current_gameState == GameState.TITLE:
        if KEYS[pygame.K_RETURN]:
            game_init(False)
            current_gameState = GameState.MAIN
        if KEYS[pygame.K_LCTRL] and KEYS[pygame.K_r]:
            confirm = pyautogui.confirm("Are you sure you want to reset the high scores?", "Confirm Reset", ["Yes", "No"])
            if confirm == "Yes":
                blanks = pyautogui.confirm("Would you like to restore the default placeholders?", "Placeholder Restore", ["Yes", "No"])
                scoreboard.c.execute("DELETE FROM HighScores;",)
                if blanks == "Yes":
                    scoreboard.reset()
                scoreboard.conn.commit()

    if current_gameState == GameState.MAIN:
        if len(bg_list) < 2:
            bg_list.append(Background(startX = random.randint(900, 1200), state=random.choice([BackState.CITY, BackState.MOUNTAINS])))
            bg_list.append(Background(startX = random.randint(1400, 2000), state=random.choice([BackState.CITY, BackState.MOUNTAINS])))

        if len(victim_list) < 4:
            victim_list.append(Victim(random.randint(900, 2000), random.randint(350, 450)))
            
        for victim in victim_list:
            victim.update()
            if player.current_state != HeroState.DEAD:
                if victim.hit_box.colliderect(player.hit_box):
                    SOUNDBOARD.play(SOUNDBOARD.rescue)
                    player.victims_saved += 1
                    player.score += 250
                    victim_list.remove(victim)
            
            if victim.hit_box.right < 0:
                victim_list.remove(victim)
                player.display.life_rect.width += 5
                player.victims_saved += 1
            
            for bullet in player.bullet_list:
                if bullet.rect.colliderect(victim.hit_box):
                    player.victims_saved -= 1
                    player.score -= 500
                    player.bullet_list.remove(bullet)
                    try:
                        SOUNDBOARD.play(SOUNDBOARD.victim_dies)
                        victim_list.remove(victim)
                        if player.score < 0:
                            player.score = 0
                            player.current_state = HeroState.DEAD
                    except ValueError:
                        pass
                        
        for lines in roadlines_list:
            lines.x -= 5
            if lines.right <= 0:
                lines.x = 1000

        # Objects' update methods go here
        for bgs in bg_list:
            bgs.update()
            if bgs.mount_image[-1].rect.x <= -50 or bgs.city_image[-1].rect.x <= -50:
                bg_list.remove(bgs)
                
        for star in starfield:
            star.update()            
        
        if len(enemy_list) < max_enemies:
            enemy_list.append(Enemy(random.randint(900, 1200), random.choice([EnemyType.BIKE, EnemyType.PLANE])))

        for enemy in enemy_list:
            enemy.update()
            if enemy.hitbox.colliderect(player.hit_box):
                SOUNDBOARD.play(SOUNDBOARD.explosion)
                player.get_hit(damage = 20)
                player.kill_count += 1
                enemy.current_state = EnemyState.DEAD
            if enemy.hitbox.right <= 0:
                enemy_list.remove(enemy)
            for bullet in enemy.bullet_list:
                for victim in victim_list:
                    if bullet.rect.colliderect(victim.hit_box):
                        try:
                            SOUNDBOARD.play(SOUNDBOARD.victim_dies)
                            victim_list.remove(victim)
                            enemy.bullet_list.remove(bullet)
                            player.display.life_rect.width -= 5
                        except ValueError:
                            pass
                if bullet.rect.colliderect(player.hit_box):
                    SOUNDBOARD.play(SOUNDBOARD.hit)
                    enemy.bullet_list.remove(bullet)
                    player.get_hit()
            for bullet in player.bullet_list:
                if bullet.rect.colliderect(enemy.hitbox):
                    SOUNDBOARD.play(SOUNDBOARD.explosion)
                    player.bullet_list.remove(bullet)
                    player.score += enemy.points
                    player.kill_count += 1
                    enemy.current_state = EnemyState.DEAD
            
            if enemy.current_state == EnemyState.DEAD:
                if enemy.enemy_type == EnemyType.BIKE:
                    if enemy.bike[0].rect.x >= 800:
                        enemy_list.remove(enemy)
                if enemy.enemy_type == EnemyType.PLANE:
                    if enemy.plane[0].rect.x >= 800:
                        enemy_list.remove(enemy)
                for bullet in enemy.bullet_list:
                    enemy.bullet_list.remove(bullet)

        if player.victims_saved % 20 == 0 and player.victims_saved != 0:
            if len(POW_list) < 1:
                POW_list.append(Pow(900, player.hit_box.y))

        for pow in POW_list:
            pow.update()
            if pow.hitbox.colliderect(player.hit_box):
                player.display.life_rect.width = player.MAX_LIFE
                SOUNDBOARD.play(SOUNDBOARD.victim_dies)
                POW_list.remove(pow)
            if pow.hitbox.right <= 0:
                POW_list.remove(pow)

        if player.display.life_rect.width >= 200:
            player.display.life_rect.width = 200
        
        if player.kill_count >= clear_count and player.current_state != HeroState.DEAD:
            current_gameState = GameState.TRANSITION

        if player.current_state == HeroState.DEAD:
            if player.dead_car[0].rect.top > 800:
                current_gameState = GameState.GAME_OVER

        player.update()

    if current_gameState == GameState.TRANSITION:
        line_0 = "Well Done!"
        line_1 = f"Victims Saved: {player.victims_saved}"
        line_2 = "Choose an Option!"
        choice = pyautogui.confirm(f"{line_0}\n{line_1}\n{line_2}", "Well Done!", ["Go to Next Level", "Play from Beginning", "Quit to OS"])
        if choice == "Go to Next Level":
            game_init()
        elif choice == "Play from Beginning":
            current_gameState = GameState.TITLE
        else:
            die()
            

    if current_gameState == GameState.GAME_OVER:
        line_0 = "You're Dead!"
        line_1 = f"Your Final Score: {player.score}"
        line_2 = f"Victims Saved: {player.victims_saved}"
        line_3 = "Choose an Option"
        choice = pyautogui.confirm(f"{line_0}\n{line_1}\n{line_2}\n{line_3}", "GAME OVER!!", ["Register High Score", "Start Again", "Quit to OS"])
        if choice == "Register High Score":
            scoreboard.register(player.score)
            current_gameState = GameState.TITLE
        elif choice == "Start Again":
            current_gameState = GameState.TITLE
        else:
            die()


    pygame.display.update()
    SURFACE.fill(BG)

def run():
    while True:
        update()

if __name__ == '__main__':
    run()