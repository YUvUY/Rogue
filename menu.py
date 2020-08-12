import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BUTTON_WIDTH = 190
BUTTON_HEIGHT = 49

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Menu:
    def __init__(self, items):
        self.items = items
        self.state = -1
        self.font = pygame.font.Font('source\\Song.ttf', 35)
        self.sprite_sheet = pygame.image.load("source\\button.png").convert()
        self.buttons = self.creat_button()
        self.rect_list = self.get_rect_list()
        self.sound_index = -1
        self.sound = pygame.mixer.Sound('source\\switch2.ogg')

    def get_button_pos(self, index):
        pos_x = (SCREEN_WIDTH // 2) - (BUTTON_WIDTH // 2)
        tol_height = len(self.items) * BUTTON_HEIGHT
        pos_y = (SCREEN_HEIGHT // 2) - (tol_height // 2) + (index * (BUTTON_HEIGHT + 10))

        return pos_x, pos_y

    def get_rect_list(self):
        rect_list = []
        for index, item in enumerate(self.items):
            pos_x, pos_y = self.get_button_pos(index)
            rect = pygame.Rect(pos_x, pos_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            rect_list.append(rect)
        return rect_list

    def creat_button(self):
        '''Get button images'''
        button_dic = {}
        button_dic['blue'] = self.get_image(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_dic['yellow'] = self.get_image(190, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        return button_dic

    def get_image(self, x, y, width, height):
        '''Get one part of a bg image'''
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image

    def get_text_pos(self, label, button_pos):
        width = label.get_width()
        height = label.get_height()
        x, y = button_pos
        pos_x = x + (BUTTON_WIDTH // 2) - (width // 2)
        pos_y = y + (BUTTON_HEIGHT // 2) - (height // 2)
        '''Stay in middle'''
        return pos_x, pos_y

    def collide(self):
        '''mouse cursor inside button'''
        index = -1
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.rect_list):
            if rect.collidepoint(mouse_pos):
                index = i
        return index

    def display_frame(self, screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                button = self.buttons['yellow']
            else:
                button = self.buttons['blue']

            label = self.font.render(item, True, WHITE)

            button_pos = self.get_button_pos(index)
            text_pos = self.get_text_pos(label, button_pos)
            screen.blit(button, button_pos)
            screen.blit(label, text_pos)

    def update(self):
        '''Update proper image and sound of button '''
        self.state = self.collide()
        if self.state != -1 and self.sound_index != self.state:
            self.sound.play()
        self.sound_index = self.state
