import pygame
import librosa
from menu import Menu
from map import Map
from pygame.locals import *
import  common_function
import tkinter
import tkinter.filedialog
from scipy import optimize
import sprite
import character
import time

FRAME_RATE = 60

ROW = 9
OFFSET_X = 15
OFFSET_Y = 15

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

'''LOWER == NEED MORE ACCUATE'''
ACCURACY = 50
'''MOVE 60 PIXEL PER STEP'''
STEP = 60
BLOCK = 60

LIVES_LEGEND = 650
MONSTER_LEGEND = 595
TEXT_LEGEND = 660

class Game():
    def __init__(self, screen, clk):
        self.heart_image = pygame.image.load('source\\heart.png')
        self.heart_empty_image = pygame.image.load('source\\heart_empty.png')
        self.hero_image = pygame.image.load('source\\TEMP_medic.png')
        self.black_image = pygame.image.load('source\\blackground.jpg')
        self.red_image = pygame.image.load('source\\redground.png')
        self.background_image = pygame.image.load('source\\menu_background.jpg').convert()
        self.mouse_image = pygame.image.load('source\\broadsword.png')
        self.divide_image = pygame.image.load('source\\border_vertical.png')
        self.ring_image = pygame.image.load('source\\ring.png')
        self.welBk_image = pygame.image.load('source\\welcome_bk.png')

        self.skeleton_static = pygame.image.load('source\\skeleton_static.png')
        self.slime_green_static = pygame.image.load('source\\slime_green_static.png')
        self.slime_blue_static = pygame.image.load('source\\slime_blue_static.png')
        self.spider_static = pygame.image.load('source\\spider_static.png')
        self.gameover = pygame.image.load('source\\game_over.png')

        self.mouse_cursor = pygame.transform.scale(self.mouse_image, (30, 30))
        self.font1 = pygame.font.Font('source\\Font Error.ttf', 18)
        self.font2 = pygame.font.Font('source\\Song.ttf', 35)
        self.font3 = pygame.font.Font('source\\Font Error.ttf', 35)
        self.menu = Menu(('START', 'HELP', 'EXIT'))
        self.font_text1 = self.font1.render('Won\'t move', True, WHITE)
        self.font_text2 = self.font1.render('Move up & down', True, WHITE)
        self.font_text3 = self.font1.render('Square movement', True, WHITE)
        self.font_text4 = self.font1.render('Sloping movement, ', True, WHITE)


        self.useless = []


        self.state = 6 #welcome
        self.screen = screen
        self.menu = Menu(('START','HELP','EXIT'))
        self.map = Map(self.screen)

        self.move = False
        self.pos_x, self.pos_y = 4, 4

        self.groups = sprite.Groups(screen, self.map)
        self.clk = clk
        self.attacked = True
        self.last_time = 0

        self.beats_time_mod = []
        self.modified_beats = []

        self.lives = 3
        self.lv = 1

        self.swipe = sprite.Animation(self.screen, 'source\\swipe_dagger.png', 3)
        self.swipe_group = pygame.sprite.Group()
        self.swipe_group.add(self.swipe)


    def game_quit(self):
        pygame.quit()
        exit()

    def selection(self):
        print(self.menu.state)

    def update_frame(self):
        common_function.check_return()
        '''Creat Background'''
        self.screen.blit(self.background_image, (0, 0))
        '''Creat Mouse Cursor '''
        x, y = pygame.mouse.get_pos()
        x -= self.mouse_cursor.get_width() / 2
        y -= self.mouse_cursor.get_height() / 2
        self.screen.blit(self.mouse_cursor, (x, y))

    def update_menu_frame(self):
        common_function.check_return()
        '''Creat Background'''
        self.screen.blit(self.background_image, (0, 0))
        '''Creat Menu'''
        self.menu.update()
        self.menu.display_frame(self.screen)
        '''Creat Mouse Cursor '''
        x, y = pygame.mouse.get_pos()
        x -= self.mouse_cursor.get_width() / 2
        y -= self.mouse_cursor.get_height() / 2
        self.screen.blit(self.mouse_cursor, (x, y))

    def update_game_frame(self):
        common_function.check_return()
        '''Display Background'''
        self.screen.blit(self.black_image, (0, 0))

        '''Draw Hero's POS'''
        rectx, recty = OFFSET_X + self.pos_x * BLOCK , OFFSET_Y + self.pos_y * BLOCK + BLOCK/2
        sqr = pygame.draw.rect(self.screen, YELLOW, (rectx, recty, 60, 60))

        '''Draw the map'''
        self.map.display_map()

        '''Creat Mouse Cursor '''
        x, y = pygame.mouse.get_pos()
        x -= self.mouse_cursor.get_width() / 2
        y -= self.mouse_cursor.get_height() / 2
        self.screen.blit(self.mouse_cursor, (x, y))

        '''Display Divide'''
        self.screen.blit(self.divide_image, (580, 0))

        '''Display Lv inf'''
        self.display_Lv()

        '''Display Lives'''
        if self.lives == 3:
            for i in range(3):
                self.screen.blit(self.heart_image, (LIVES_LEGEND + i * 50, 15))
        elif self.lives == 2:
            self.screen.blit(self.heart_image, (LIVES_LEGEND + 0 * 50, 15))
            self.screen.blit(self.heart_image, (LIVES_LEGEND + 1 * 50, 15))
            self.screen.blit(self.heart_empty_image, (LIVES_LEGEND + 2 * 50, 15))
        elif self.lives == 1:
            self.screen.blit(self.heart_image, (LIVES_LEGEND + 0 * 50, 15))
            self.screen.blit(self.heart_empty_image, (LIVES_LEGEND + 1 * 50, 15))
            self.screen.blit(self.heart_empty_image, (LIVES_LEGEND + 2 * 50, 15))
        else:
            for i in range(3):
                self.screen.blit(self.heart_empty_image, (LIVES_LEGEND + i * 50, 15))

        '''Display monster images'''
        self.screen.blit(self.slime_green_static, (MONSTER_LEGEND, 220))
        self.screen.blit(self.slime_blue_static, (MONSTER_LEGEND, 320))
        self.screen.blit(self.spider_static, (MONSTER_LEGEND, 420))
        self.screen.blit(self.skeleton_static, (MONSTER_LEGEND, 520))

        '''Display monster information'''
        self.screen.blit(self.font_text1, (TEXT_LEGEND, 240))
        self.screen.blit(self.font_text2, (TEXT_LEGEND, 340))
        self.screen.blit(self.font_text3, (TEXT_LEGEND, 440))
        self.screen.blit(self.font_text4, (TEXT_LEGEND, 540))


        '''check beat'''
        clk = pygame.mixer.music.get_pos()
        if int(clk/10) in self.beats_time_mod or int(clk/10) + 1 in self.beats_time_mod or int(clk/10) - 1 in self.beats_time_mod:
            if int(clk / 10) in self.beats_time_mod:
                self.beats_time_mod.remove(int(clk / 10))
            elif int(clk / 10) + 1 in self.beats_time_mod:
                self.beats_time_mod.remove(int(clk / 10) + 1)
            else:
                self.beats_time_mod.remove(int(clk / 10) - 1)
            #print(int(clk/10))
            self.move = True

        '''Display Monsters'''
        ticks = pygame.time.get_ticks()  # Give gif clk
        self.groups.monster_group.update(ticks, 0, 0, self.move)
        self.move = False
        self.groups.monster_group.draw(self.screen)

        '''Check and display attacked'''
        self.check_attacked()
        if self.attacked:
            self.screen.blit(self.red_image, (0, 0))
        if pygame.time.get_ticks() > self.last_time + 500:
            self.attacked = False


        '''Display Hero'''
        self.screen.blit(self.ring_image, (rectx, recty + 10))
        self.groups.hero_group.update(ticks, self.pos_x, self.pos_y)
        self.groups.hero_group.draw(self.screen)

        if self.swipe.visable:
            self.swipe_group.update(ticks)
            self.swipe_group.draw(self.screen)

    def display_Lv(self):
        lv = 'LEVEL ' + str(self.lv)
        label = self.font3.render(lv, True, YELLOW)
        width = label.get_width()
        height = label.get_height()
        pos_x = 800 - 20 - width
        pos_y = 80
        self.screen.blit(label, (pos_x, pos_y))

    '''
           STATE:
           1           MENU
           2           START
           3           HELP
           4           EXIT
           5           GAME OVER
           6           WELCOME
           0           GAME RUNNING
    '''

    def state_logic(self):
        if self.state == 0:
            self.show_game_process()
            return False
        elif self.state == 1:
            self.show_menu()
            return False
        elif self.state == 2:
            self.show_game()
            return False
        elif self.state == 3:
            self.show_help()
            return False
        elif self.state == 4:
            return True
        elif self.state == 5:
            self.display_gameover()
        elif self.state == 6:
            self.welcome()

    def welcome(self):
        text = self.font2.render("(按任意键以继续)", True, WHITE, BLACK)
        ztx, zty, ztw, zth = text.get_rect()
        jx = pygame.Rect(800, 200, ztw, zth)
        clock = pygame.time.Clock()

        txt1 = self.font2.render("一名探险家偶然踏入一座地牢，神奇的是: ", True, WHITE, BLACK)
        txt2 = self.font2.render("这座地牢的里的怪物们会根据音乐节奏移动。", True, WHITE, BLACK)
        txt3 = self.font2.render("小心移动并击杀怪物，逃出地牢···", True, WHITE, BLACK)
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.welBk_image, (100, 300))
        self.screen.blit(txt1,(50,50))
        self.screen.blit(txt2,(50,150))
        self.screen.blit(txt3,(50,250))
        pygame.display.update()
        time.sleep(3)
        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.welBk_image, (100, 300))
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    self.state = 1
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = 1
                    return
            jx.x -= 5
            if jx.x < 0 - ztw:
                jx.x = 510
            self.screen.blit(text, [jx.x, jx.y])
            pygame.display.update()

    def show_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_quit()
            if event.type == pygame.KEYDOWN:
                if event.type == K_ESCAPE:
                    self.game_quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.menu.rect_list[0].collidepoint(mouse_x, mouse_y):
                    self.state = 2
                elif self.menu.rect_list[1].collidepoint(mouse_x, mouse_y):
                    self.state = 3
                elif self.menu.rect_list[2].collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    exit()
                else:
                    self.state = 1
        self.update_menu_frame()
        pygame.display.flip()

    def display_message(self, message):
        label = self.font2.render(message, True, WHITE)
        width = label.get_width()
        height = label.get_height()
        pos_x = (SCREEN_WIDTH // 2) - (width // 2)
        pos_y = (SCREEN_HEIGHT // 2) - (height // 2)

        self.screen.blit(label, (pos_x, pos_y))

    def show_help(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    print("Exit from help")
                    self.state = 1
                    return
        self.update_frame()
        label1 = self.font2.render("  使用←↑→↓移动   ", True, WHITE)
        label2 = self.font2.render("开始前选择地牢节奏", True, WHITE)
        label3 = self.font2.render("怪物将根据节奏移动", True, WHITE)
        label4 = self.font2.render("(按ESC回到主菜单)", True, WHITE)
        pos_x = 150
        pos_y = 200
        self.screen.blit(label1, (pos_x, pos_y))
        self.screen.blit(label2, (pos_x, pos_y + 50))
        self.screen.blit(label3, (pos_x, pos_y + 100))
        self.screen.blit(label4, (pos_x + 100, pos_y + 300))

        pygame.display.flip()

    def select_music(self):
        root = tkinter.Tk()
        root.withdraw()
        music_name = tkinter.filedialog.askopenfilenames()
        if len(music_name) != 0:
            music_name_str = ''
            for i in range(0, len(music_name)):
                music_name_str += str(music_name[i])
            print(music_name_str)
            return music_name_str
        else:
            self.update_frame()
            self.display_message("Please select your music !")
            pygame.display.flip()
            self.select_music()

    def show_game(self):
        common_function.check_return()

        filename = self.select_music()

        pygame.display.flip()

        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_endevent(pygame.USEREVENT+1)
        '''Beat Track'''
        y, sr = librosa.load(filename)
        duration = librosa.get_duration(y)
        #print(duration)
        tempo, beats = librosa.beat.beat_track(y)
        amt = beats.size

        beats_time = librosa.frames_to_time(beats)
        # print(beats_time)
        self.beats_time_mod = []
        for b in beats_time:
            self.beats_time_mod.append(int(b * 100))

        self.state = 0
        pygame.mixer.music.play(1, 0)
        self.show_game_process()

    def display(self):
        if self.state == 0:
            self.update_game_frame()

        else:
            self.update_frame()
        self.clk.tick(FRAME_RATE)

    def display_gameover(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game_quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    #print("Exit from gameover")
                    self.state = 1
                    return
        #print('gameover')
        self.screen.blit(self.gameover, (0, 0))
        label4 = self.font2.render("(按ESC回到主菜单)", True, WHITE)
        self.screen.blit(label4, (250, 500))

        pygame.display.flip()


    def resetPos(self):
        for monster in self.groups.monster_group:
            #print(monster.pos_x, monster.pos_y)
            self.map.array[monster.pos_x][monster.pos_x] = 1

    def readPos(self):
        self.map = Map(self.screen)
        for monster in self.groups.monster_group:
            #print(monster.pos_x, monster.pos_y)
            self.map.array[monster.pos_x][monster.pos_y] = 2

    def removeMonster(self, pos_x, pos_y):
        for monster in self.groups.monster_group:
            if monster.pos_x == pos_x and monster.pos_y == pos_y:
                #print(pos_x, pos_y)
                self.map.array[pos_x][pos_y] = 1
                self.groups.monster_group.remove(monster)

    def move_or_kill(self, factor_x, factor_y):
        if common_function.check_movable(self.pos_x + factor_x, self.pos_y + factor_y, self.map):
            '''Kill'''
            if self.map.array[self.pos_x + factor_x][self.pos_y + factor_y] == 2:

                self.swipe.set_pos(self.pos_x + factor_x, self.pos_y + factor_y)
                self.swipe.visable = True

                self.removeMonster(self.pos_x + factor_x, self.pos_y + factor_y)

            else:
                '''Move'''
                self.pos_x += factor_x
                self.pos_y += factor_y
                #self.move = True

    def check_attacked(self):
        self.readPos()
        #common_function.printMap(self.map)

        if self.map.array[self.pos_x][self.pos_y] == 2:
            '''Was attacked'''
            self.lives -= 1
            if self.lives == 0:
                pygame.mixer.music.stop()
                self.__init__(self.screen, self.clk)
                self.state = 5
                self.display_gameover()
            self.attacked = True
            self.last_time = pygame.time.get_ticks()
            flag = False
            while not flag:
                temp_x = common_function.get_randint(1,8)
                temp_y = common_function.get_randint(1,8)
                if self.map.array[temp_x][temp_y] == 1:
                    self.pos_x = temp_x
                    self.pos_y = temp_y
                    flag = True

    def get_proper_pos(self):
        while True:
            temp_x = common_function.get_randint(1, 8)
            temp_y = common_function.get_randint(1, 8)
            if self.map.array[temp_x][temp_y] == 1:
                return temp_x, temp_y

    def add_characters_1(self):
        pos_x , pos_y = self.get_proper_pos()
        self.map.array[pos_x][pos_y] = 2
        green_slime = character.Slime_Green(self.screen, pos_x, pos_y, self.map)
        self.groups.monster_group.add(green_slime)

    def add_characters_2(self):
        pos_x, pos_y = self.get_proper_pos()
        self.map.array[pos_x][pos_y] = 2
        blue_slime = character.Slime_Blue(self.screen, pos_x, pos_y, self.map)
        self.groups.monster_group.add(blue_slime)

    def add_characters_3(self):
        pos_x, pos_y = self.get_proper_pos()
        self.map.array[pos_x][pos_y] = 2
        spider = character.Spider(self.screen, pos_x, pos_y, self.map)
        self.groups.monster_group.add(spider)

    def add_characters_4(self):
        pos_x, pos_y = self.get_proper_pos()
        self.map.array[pos_x][pos_y] = 2
        skeleon = character.Skeleon(self.screen, pos_x, pos_y, self.map)
        self.groups.monster_group.add(skeleon)

    def auto_add_monster(self):
        if self.lv == 2:
            self.add_characters_2()
        elif self.lv == 3:
            self.add_characters_3()
        elif self.lv == 4:
            self.add_characters_4()
        else:
            for i in range(self.lv-4):
                raint = common_function.get_randint(1,4)
                if raint == 1:
                    self.add_characters_1()
                elif raint == 2:
                    self.add_characters_2()
                elif raint == 3:
                    self.add_characters_3()
                else:
                    self.add_characters_4()


    def level_up(self):
        print("Level up")
        self.lv += 1
        self.auto_add_monster()


    def show_game_process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mixer.music.stop()
                    self.__init__(self.screen, self.clk)
                    self.state = 1
                    return

                else:
                    self.readPos()
                    #common_function.printMap(self.map)

                    if event.key == K_LEFT or event.key == K_a:
                        self.move_or_kill(-1, 0)

                    elif event.key == K_RIGHT or event.key == K_d:
                        # 右方向键则加一
                        self.move_or_kill(+1, 0)

                    elif event.key == K_UP or event.key == K_w:
                        # 类似
                        self.move_or_kill(0, -1)

                    elif event.key == K_DOWN or event.key == K_s:
                        self.move_or_kill(0, +1)
                if not len(self.groups.monster_group):
                    self.level_up()

            if event.type == pygame.USEREVENT+1:
                print("Game Finished")
                self.state = 1
                return

        pygame.display.flip()


