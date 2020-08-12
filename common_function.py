import pygame, math
from map import Map
import random

ROW = 9
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def get_randint(a, b):
    return random.randint(a, b)

def f_linear(x, a, b):
  return a * x + b


def load_images(sprite_sheet, width, height):
    """ This method will return a list with the images """
    # Create a list that will contain the images
    image_list = []
    # Go through every single image in the sprite sheet
    for y in range(0, sprite_sheet.get_height(), height):
        for x in range(0, sprite_sheet.get_width(), width):
            # load images into a list
            img = get_image(sprite_sheet, x, y, width, height)
            image_list.append(img)
    return image_list


def get_image(sprite_sheet, x, y, width, height):
    """ This method will cut an image and return it """
    # Create a new blank image
    image = pygame.Surface([width, height]).convert()
    # Copy the sprite from the large sheet onto the smaller
    image.blit(sprite_sheet, (0, 0), (x, y, width, height))
    # Assuming black works as the transparent color
    image.set_colorkey(BLACK)
    # Return the image
    return image


def get_degrees(pos):
    x = pos[0] - SCREEN_WIDTH // 2
    y = pos[1] - SCREEN_HEIGHT // 2
    degrees = 0
    if y < 0:
        if x == 0:
            degrees = 90
        elif x > 0:
            tmp = math.atan(abs(y) / abs(x))
            degrees = math.degrees(tmp)
        else:
            tmp = math.atan(abs(y) / abs(x))
            degrees = 180 - math.degrees(tmp)
    elif y > 0:
        if x == 0:
            degrees = 270
        elif x > 0:
            tmp = math.atan(abs(y) / abs(x))
            degrees = 360 - math.degrees(tmp)
        else:
            tmp = math.atan(abs(y) / abs(x))
            degrees = 180 + math.degrees(tmp)
    elif x < 0:
        degrees = 180

    return degrees


def check_return():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

            exit()


def check_movable(pos_x, pos_y, map):
    if map.array[pos_x][pos_y] == 1 or map.array[pos_x][pos_y] == 2:
        return True
    else:
        return False



def printMap(map):
    for i in range(len(map.array)):
        print(map.array[i])
    print()