import pygame
from game import Game
from pygame.locals import *
from sys import exit

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_RATE = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Rogue')
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    game = Game(screen, clock)

    game_done = False



    while not game_done:

        '''game.show_menu()'''

        game_done = game.state_logic()

        game.display()



if __name__ == '__main__':
    main()