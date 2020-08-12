import pygame

class GameRun():
    def __init__(self, filename):
        self.score = 0
        self.music = pygame.mixer.music.load(filename)

    def start(self):
        pygame.mixer.music.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
