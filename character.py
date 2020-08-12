import pygame
from pygame.locals import *
import map
import common_function as cf

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

ROW = 9

OFFSET_X = 15
OFFSET_Y = 15

BLOCK = 60
FRAME_RATE = 400


class Character(pygame.sprite.Sprite):
    def __init__(self, screen, filename, pos_x, pos_y, width, height, cols, map):
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
        self.cols =1
        self.map = map
        self.load(filename, pos_x, pos_y, width, height, cols)
        self.old_x = pos_x
        self.old_y = pos_y
        self.offset_x = 0
        self.offset_y = 0

    def load(self, filename,pos_x, pos_y, width, height, cols):
        self.master_image = pygame.image.load(filename)
        self.frame_width = width
        self.frame_height = height
        self.rect = pos_x * BLOCK + OFFSET_X, pos_y * BLOCK + OFFSET_Y, width, height
        self.cols = cols
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, pos_x, pos_y):
        if current_time >= self.last_frame + FRAME_RATE:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_frame = current_time

        if self.first_frame != self.old_frame:
            frame_x = (self.frame % self.cols) * self.frame_width
            rect = (frame_x, 0, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

        self.rect = pos_x * BLOCK + OFFSET_X, pos_y * BLOCK + OFFSET_Y, self.frame_width, self.frame_height


class Hero(Character):
    def __init__(self, screen, pos_x, pos_y, map):
        super().__init__(screen, 'source\\TEMP_medic.png', pos_x, pos_y, BLOCK, BLOCK, 2, map)

    def update(self, current_time, pos_x=0, pos_y=0, is_move = False):
        if cf.check_movable(pos_x, pos_y, self.map):
            super().update(current_time, pos_x, pos_y)


class Slime_Green(Character):
    def __init__(self, screen, pos_x, pos_y, map):
        super().__init__(screen, 'source\\slime_green.png', pos_x, pos_y, BLOCK, BLOCK, 4, map)

    def update(self, current_time, pos_x=0, pos_y=0, is_move=False):
        super().update(current_time, self.pos_x, self.pos_y)


class Slime_Blue(Character):
    def __init__(self, screen, pos_x, pos_y, map):
        super().__init__(screen, "source\\slime_blue.png", pos_x, pos_y, BLOCK, BLOCK, 8, map)
        self.flag = 1
        self.cnt = 0

    def update(self, current_time, pos_x=0, pos_y=0, is_move=False):
        if is_move:
            self.cnt += 1
            if self.cnt%2 == 0:
                if cf.check_movable(self.pos_x, self.pos_y + self.flag, self.map):
                    self.pos_y += self.flag
                    self.flag = - self.flag
                    super().update(current_time, self.pos_x, self.pos_y)
                else:
                    super().update(current_time, self.pos_x, self.pos_y)
        else:
            super().update(current_time, self.pos_x, self.pos_y)


class Spider(Character):
    def __init__(self, screen, pos_x, pos_y, map):
        super().__init__(screen, "source\\spider.png", pos_x, pos_y, BLOCK, BLOCK, 5, map)
        self.move = [(0,1), (1,0), (0,-1), (-1,0)]
        self.flag = 3

    def update(self, current_time, pos_x=0, pos_y=0, is_move=False):
        if is_move:
            temp_flag = (self.flag + 1) % 4
            temp_x = self.pos_x + self.move[temp_flag][0]
            temp_y = self.pos_y + self.move[temp_flag][1]
            if cf.check_movable(temp_x, temp_y, self.map):
                self.flag = temp_flag
                self.pos_x = temp_x
                self.pos_y = temp_y

                super().update(current_time, self.pos_x, self.pos_y)
        else:
            super().update(current_time, self.pos_x, self.pos_y)


class Skeleon(Character):
    def __init__(self, screen, pos_x, pos_y, map):
        super().__init__(screen, "source\\skeleton.png", pos_x, pos_y, BLOCK, BLOCK, 8, map)
        self.dir_x = 1
        self.dir_y = 1
        self.flag = 1

    def determine_dir(self):
        while not cf.check_movable(self.pos_x+self.dir_x, self.pos_y+self.dir_y, self.map):
            if self.flag == 1:
                self.dir_x = -self.dir_x
                self.flag = -1
            else:
                self.dir_y = -self.dir_y
                self.flag = 1

    def update(self, current_time, pos_x, pos_y, is_move=False):
        if is_move:
            self.determine_dir()
            self.pos_x += self.dir_x
            self.pos_y += self.dir_y
        super().update(current_time, self.pos_x, self.pos_y)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    pygame.display.set_caption("精灵类测试")
    font = pygame.font.Font(None, 18)
    framerate = pygame.time.Clock()

    cat = Character(screen, 'source\\slime_green.png', BLOCK, BLOCK, BLOCK, BLOCK, 4 )
    group = pygame.sprite.Group()
    group.add(cat)

    while True:
        ticks = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            exit()

        screen.fill((0, 0, 100))

        group.update(ticks)
        group.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()