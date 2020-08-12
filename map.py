import pygame
from pygame.locals import *

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

class Map():
    def __init__(self, screen):
        '''MAP: 9 * 9   WALL:0 FLOOR:1  60PIXEL PER IMAGE'''
        self.screen = screen

        self.floor_image = pygame.image.load('source\\new_floor.png')
        self.wall_mage = pygame.image.load('source\\wall.png')

        self.array = self.get_array()

    def display_map(self):
        for i in range(ROW):
            if not i:
                for j in range(ROW):
                    if self.array[i][j] == 0:
                        self.screen.blit(self.wall_mage, (OFFSET_X + j * BLOCK, OFFSET_Y + i))
                    else:
                        self.screen.blit(self.floor_image, (OFFSET_X + j * BLOCK, OFFSET_Y + i + BLOCK / 2))
            else:
                for j in range(ROW):
                    if self.array[i][j] == 0:
                        self.screen.blit(self.wall_mage, (OFFSET_X + j * BLOCK, OFFSET_Y + i * BLOCK))
                    else:
                        self.screen.blit(self.floor_image, (OFFSET_X + j * BLOCK, OFFSET_Y + i * BLOCK + BLOCK / 2))

    def get_array(self):
        new_ary = []
        for i in range(ROW):
            ary_line = []
            if i == 0 or i == ROW-1 :
                for j in range(int(ROW/2)):
                    ary_line.append(0)
                ary_line.append(-1)
                for j in range(int(ROW/2)):
                    ary_line.append(0)
            elif i == int(ROW/2):
                ary_line.append(-1)
                for j in range(ROW-2):
                    ary_line.append(1)
                ary_line.append(-1)

            else:
                ary_line.append(0)
                for j in range(ROW-2):
                    ary_line.append(1)
                ary_line.append(0)
            new_ary.append(ary_line)
        return new_ary


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Game')
    mp = Map(screen)
    framerate = pygame.time.Clock()
    while True:
        framerate.tick(CHARACTER_FRAME_RATE)
        ticks = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        mp.display_map()
        mp.group.update(ticks)
        mp.group.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()