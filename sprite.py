import pygame
import character
import common_function as cf

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

EDGE = 20
BLOCK = 60

ROW = 9
OFFSET_X = 15
OFFSET_Y = 15
CHARACTER_FRAME_RATE = 3
FRAME_RATE = 30


class Animation(pygame.sprite.Sprite):
    def __init__(self, screen, filename, cols, pos_x = 0, pos_y = 0, width = 60, height= 60):
        pygame.sprite.Sprite.__init__(self)

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.screen = screen
        self.image = None
        self.master_image = None
        self.rect = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.cols = cols
        self.load(filename, pos_x, pos_y, width, height, cols)
        self.visable = False

    def load(self, filename,pos_x, pos_y, width, height, cols):
        self.master_image = pygame.image.load(filename)
        self.frame_width = width
        self.frame_height = height
        self.rect = pos_x * BLOCK + OFFSET_X, pos_y * BLOCK + OFFSET_Y, width, height
        self.cols = cols
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    # last number is frame rate
    def update(self, current_time):
        if self.visable:
            if current_time >= self.last_frame + 20:
                self.frame += 1
                if self.frame > self.last_frame:
                    self.frame = self.first_frame
                self.last_frame = current_time

            if self.first_frame != self.old_frame:
                if not (self.frame+1) % self.cols:
                    self.visable = False
                frame_x = (self.frame % self.cols) * self.frame_width
                rect = (frame_x, 0, self.frame_width, self.frame_height)
                self.image = self.master_image.subsurface(rect)
                self.old_frame = self.frame

            self.rect = self.pos_x * BLOCK + OFFSET_X, self.pos_y * BLOCK + OFFSET_Y, self.frame_width, self.frame_height


    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y



class Groups():
    def __init__(self, screen, map):
        self.screen = screen
        self.monster_group = pygame.sprite.Group()
        self.hero_group = pygame.sprite.Group()
        self.map = map
        hero = character.Hero(self.screen, 4, 4, self.map)
        self.hero_group.add(hero)
        green_slime = character.Slime_Green(self.screen, 3, 3, self.map)
        self.monster_group.add(green_slime)


