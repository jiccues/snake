#-*-coding:utf-8-*-


import pygame
import random


class Vector2:
    x = 0
    y = 0

    def __init__(self, _x=0, _y=0):
        self.x = _x
        self.y = _y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)


class Config:
    #map
    game_map_size = Vector2(20, 20)
    cell_size = Vector2(20, 20)
    snack_long = 5
    #color
    background_color = (255, 255, 255)
    snack_head_color = (0, 0, 0)
    snack_body_color = (127, 127, 127)
    bean_color = (255, 255, 0)
    #timer
    framerate = 50
    falltimes = 100


class Screen:
    name = "Snake"

    def __init__(self):
        self.size = (Config.game_map_size.x * Config.cell_size.x,
                     Config.game_map_size.y * Config.cell_size.y)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.name)


class Timer:
    time = 0
    def __init__(self):
        self.framerate = Config.framerate
        self.falltimes = Config.falltimes
        self.clock = pygame.time.Clock()


class Snake_head:
    direction = 0
    move_list = [Vector2(1, 0), Vector2(0, -1), Vector2(-1, 0), Vector2(0, 1)]
    position = Vector2()

    def __init__(self, _base):
        self.base = _base

    def refresh(self, _position):
        self.position = _position
        self.temp_direction = 0
        self.direction = self.temp_direction
        self.long = Config.snack_long

    def move(self):
        self.direction = self.temp_direction
        self.position += self.move_list[self.direction]
        self.position.x %= self.base.size.x
        self.position.y %= self.base.size.y
        if (self.base.map_list[self.position.x][self.position.y] == 0):
            self.base.map_list[self.position.x][self.position.y] = self.long + 1
            return 0
        elif self.base.map_list[self.position.x][self.position.y] == -1:
            self.long += 1
            self.base.map_list[self.position.x][self.position.y] = self.long
            return 1
        else:
            return -1


class Map:
    def __init__(self):
        self.size = Config.game_map_size
        self.snack_head = Snake_head(self)
        self.refresh()

    def refresh(self):
        self.map_list = [[0 for j in range(self.size.y)] for i in range(self.size.x)]
        self.snack_head.refresh(Vector2(self.size.x // 2, self.size.y // 2))
        self.bean()

    def move(self):
        ret = self.snack_head.move()
        if ret == -1:
            return -1
        elif ret == 0:
            for i in range(0, self.size.x):
                for j in range(0, self.size.y):
                    if self.map_list[i][j] > 0:
                        self.map_list[i][j] -= 1
            return 0
        else:
            return self.bean()

    def bean(self):
        open_space_list = []
        for i in range(0, self.size.x):
            for j in range(0, self.size.y):
                if self.map_list[i][j] == 0:
                    open_space_list.append(Vector2(i, j))
        list_len = len(open_space_list)
        if list_len == 0:
            return 1
        position = open_space_list[random.randrange(list_len)]
        self.map_list[position.x][position.y] = -1
        return 0


def main():
    pygame.init()
    screen = Screen()
    timer = Timer()
    map = Map()

    while True:
        for event in pygame.event.get():

            #quit
            if event.type == pygame.QUIT:
                print("You exit!\nYour score : %d" % (map.snack_head.long - Config.snack_long))
                pygame.quit()
                return
            
            #move
            if event.type == pygame.KEYDOWN:
                presseds = pygame.key.get_pressed()
                if ((presseds[pygame.K_UP] or presseds[pygame.K_w]) and
                    map.snack_head.direction != 3):
                    map.snack_head.temp_direction = 1
                if ((presseds[pygame.K_DOWN] or presseds[pygame.K_s]) and
                    map.snack_head.direction != 1):
                    map.snack_head.temp_direction = 3
                if ((presseds[pygame.K_LEFT] or presseds[pygame.K_a]) and
                    map.snack_head.direction != 0):
                    map.snack_head.temp_direction = 2
                if ((presseds[pygame.K_RIGHT] or presseds[pygame.K_d]) and
                    map.snack_head.direction != 2):
                    map.snack_head.temp_direction = 0
        
        #timer
        timer.time += timer.clock.tick(timer.framerate)
        if timer.time >= timer.falltimes:
            timer.time -= timer.falltimes
            move_ret = map.move()
            if move_ret == -1:
                print("You lost!\nYour score : %d" % (map.snack_head.long - Config.snack_long))
                pygame.quit()
                return
            if move_ret == 1:
                print("You win!\nYour score : %d" % (map.snack_head.long - Config.snack_long))
                pygame.quit()
                return

        #display
        screen.screen.fill(Config.background_color)
        for i in range(map.size.x):
            for j in range(map.size.y):
                rect_value = (Config.cell_size.x * i, Config.cell_size.y * j,
                              Config.cell_size.x, Config.cell_size.y)
                if map.map_list[i][j] == map.snack_head.long:
                    pygame.draw.rect(screen.screen, Config.snack_head_color, rect_value, 0)
                elif map.map_list[i][j] == -1:
                    pygame.draw.rect(screen.screen, Config.bean_color, rect_value, 0)
                elif map.map_list[i][j] > 0:
                    pygame.draw.rect(screen.screen, Config.snack_body_color, rect_value, 0)
        
        pygame.display.flip()


if __name__ == "__main__":
    main()
