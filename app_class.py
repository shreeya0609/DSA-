import pygame
import sys
import copy
from os import path
from settings import *
from player_class import *
from enemy_class import *

pygame.init()
vec = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'Start'
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.load()
        self.high_score = self.high_score_value
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()

    def run(self):
        while self.running:
            if self.state == 'Start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'Playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
                self.paused = False
            elif self.state == 'Game Over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

############################ HELPER FUNCTIONS ##################################

    def draw_text(self, words, screen, position, size, colour, font_name, centered = False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            position[0] = position[0]-text_size[0]//2
            position[1] = position[1]-text_size[1]//2
        screen.blit(text, position)

    def load(self):
        self.backgroundlogo = pygame.image.load('19BEE0182_CHESSPROJECT/pacmanlogo.jpg')
        self.backgroundlogo = pygame.transform.scale(self.backgroundlogo, (299, 66))
        self.backgroundintro = pygame.image.load('19BEE0182_CHESSPROJECT/logo.jpg')
        self.backgroundintro = pygame.transform.scale(self.backgroundintro, (405, 720))
        self.backgroundmain = pygame.image.load('19BEE0182_CHESSPROJECT/maze.png')
        self.backgroundmain = pygame.transform.scale(self.backgroundmain, (MAZE_WIDTH, MAZE_HEIGHT))

        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_File), 'r') as f:
            try:
                self.high_score_value = int(f.read())
            except:
                self.high_score_value = 0

        # Opening walls file
        # Creating walls list with co-ords of walls stored as a vector
        with open("19BEE0182_CHESSPROJECT/Walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.backgroundmain, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0),
                             (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height),
                             (WIDTH, x*self.cell_height))

        # for coin in self.coins:
        #     pygame.draw.rect(self.background, (167, 179, 34), (coin.x*self.cell_width,
        #                                                        coin.y*self.cell_height, self.cell_width, self.cell_height))

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.high_score = self.high_score_value
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open("Walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "Playing"

########################### INTRO FUNCTIONS ####################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'Playing'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.backgroundintro, (TOP_BOTTOM_BUFFER//2 + 85, TOP_BOTTOM_BUFFER//2 - 20))
        self.screen.blit(self.backgroundlogo, (TOP_BOTTOM_BUFFER//2 + 140, TOP_BOTTOM_BUFFER//2 + 100))
        self.draw_text('PUSH SPACE-BAR TO PLAY', self.screen, [WIDTH//2-1, HEIGHT//2 + 300],
                       START_TEXT_SIZE, (238, 0, 0), START_FONT, centered=True)
        self.draw_text('SINGLE PLAYER', self.screen, [WIDTH//2, HEIGHT//2 + 250],
                       START_TEXT_SIZE, (100, 149, 237), START_FONT, centered=True)
        self.draw_text('HIGH SCORE: {}'.format(self.high_score_value), self.screen, [4, 0],
                       START_TEXT_SIZE, WHITE, START_FONT)
        pygame.display.update()

########################### PLAYING FUNCTIONS ##################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.move(vec(0, 1))
                if event.key == pygame.K_p:
                    self.pause()
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.backgroundmain, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        # self.draw_grid()

        if self.player.current_score > self.high_score:
            self.high_score = self.player.current_score
            with open(path.join(self.dir, HS_File), 'w') as f:
                f.write(str(self.high_score))

        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score),
                       self.screen, [40, 0], 24, WHITE, START_FONT)
        self.draw_text('HIGH SCORE: {}'.format(self.high_score), self.screen, [WIDTH//2 + 80, 0],
                       24, WHITE, START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "Game Over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (255, 255, 0),
                               (int(coin.x*self.cell_width) + self.cell_width//2 + TOP_BOTTOM_BUFFER//2,
                                int(coin.y*self.cell_height) + self.cell_height//2 + TOP_BOTTOM_BUFFER//2), 5)

########################### PAUSE FUNCTIONS ################################

    def pause(self):
        self.paused = True
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    self.paused = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
            self.screen.fill(BLACK)
            self.draw_text("GAME PAUSED", self.screen, [WIDTH//2, 300], 52, WHITE, "rockwell",
                           centered = True)
            self.draw_text("PRESS C TO CONTINUE", self.screen, [WIDTH//2, HEIGHT//2 + 240],
                           36, (190, 190, 190), "rockwell", centered = True)
            self.draw_text("PRESS ESC TO QUIT", self.screen, [WIDTH//2, HEIGHT//1.5 + 190],
                           36, (190, 190, 190), "rockwell", centered = True)
            pygame.display.update()

########################### GAME OVER FUNCTIONS ################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.screen, [WIDTH//2, 300],  52, RED, "rockwell", centered = True)
        self.draw_text("PRESS SPACE-BAR TO PLAY AGAIN", self.screen, [WIDTH//2, HEIGHT//2+240],
                       36, (190, 190, 190), "rockwell", centered = True)
        self.draw_text("PRESS ESC TO QUIT", self.screen, [WIDTH//2, HEIGHT//1.5+190],
                       36, (190, 190, 190), "rockwell", centered = True)
        pygame.display.update()
