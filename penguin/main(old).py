import os
import pygame
from functions import rotate_map
from levels import levels, paths, goals, firsts
import random


def deci(num):
    num = str(num)
    pow = len(num) - 1
    f_num = 0

    for i in num:
        f_num += int(i) * (12 ** pow)
        pow -= 1

    return f_num


def rotate(args):
    for arg in args:
        arg.rect.x, arg.rect.y = screen_size[0] - arg.rect.y - deci(arg.size[0]), arg.rect.x
    return args


def rotate_end(end):
    end.x, end.y = screen_size[0] - end.y - 48, end.x
    return end


def rotate_pointer(p):
    for i in range(3):
        p[2 * i], p[2 * i + 1] = 488 - p[2 * i + 1], p[2 * i]
    return p


# Class for the orange dude
class Player(object):

    def __init__(self, first):
        self.enemy = False
        self.top_side = "u"
        self.size = [40, 40]
        # self.Blue_P = pygame.image.load("img/Blue_Penguin.png")
        # self.Blue_P.convert()
        # self.rect = self.Blue_P.get_rect()
        self.rect = pygame.Rect(first[0], first[1], self.size[0], self.size[1])
        # self.rect.center=(256,308)
        # self.rect.size=(self.size[0],self.size[1])
        # self.rect.x=148
        # self.rect.y=148

    def move(self, dx, dy):

        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom

        for score in scores:
            if self.rect.colliderect(score.rect):
                if self.enemy and score.value == 200:
                    score.value -= 160
                score.enable = True


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Wall(object):

    def __init__(self, pos, direction):
        walls.append(self)
        if direction == "vertical":
            self.rect = pygame.Rect(pos[0] + 40, pos[1], 8, deci(40))
        if direction == "horizontal":
            self.rect = pygame.Rect(pos[0], pos[1] + 40, deci(40), 8)


class Score(object):
    def __init__(self, pos):
        scores.append(self)
        self.value = 200
        self.size = [4, 4]
        self.enable = False
        self.rect = pygame.Rect(pos[0], pos[1], 4, 4)


o_penguin = pygame.image.load("img/Orange_Penguin.png")
b_penguin = pygame.image.load("img/Blue_Penguin.png")
fish = pygame.image.load("img/clownfish-clip-art-publicdomainvectors.png")
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
screen_size = [488, 488]
BackGround = Background('img/water_room.png', [0,0])


def Game(i):
    level = levels[i]
    goal = goals[i]
    first = firsts[i]
    path = paths[i]
    pygame.display.set_caption("Game")
    screen = pygame.display.set_mode(screen_size)

    clock = pygame.time.Clock()
    player = Player(first)
    enemy = Player(first)
    enemy.enemy = True
    end_rect = pygame.Rect(goal[0], goal[1], 40, 40)

    def make_walls():
        i = j = 76
        global walls
        walls = []
        for row in level:
            for col in row:
                if col == "v":
                    Wall((i, j), "vertical")
                elif col == "h":
                    Wall((i, j), "horizontal")
                elif col == "b":
                    Wall((i, j), "horizontal")
                    Wall((i, j), "vertical")
                if col == "E":
                    end_rect = pygame.Rect(i, j, 40, 40)
                i += deci(40)
            j += deci(40)
            i = 76

    def make_score():
        i = j = 76
        global scores
        scores = []
        for row in path:
            for col in row:
                if col == "f":
                    Score((i + 22, j + 22))
                i += deci(40)
            j += deci(40)
            i = 76

    font = pygame.font.Font('freesansbold.ttf', 32)
    textX = 10
    textY = 10

    def show_score(i, j, s):
        score_ren = font.render("Score: " + str(s), True, (255, 255, 255))
        screen.blit(score_ren, (i, j))

    def calculate_score():
        sums = 0
        for i in scores:
            sums += i.value
        return sums

    timer = -3000
    angle = "up"
    n = 0
    x = 2
    y = 0
    p = [40, screen_size[0]/2 - 10, 40, screen_size[0]/2 + 10, 25, screen_size[0]/2]
    rotate_pointer(p)
    make_score()
    running = True
    while running:

        clock.tick(100)
        angle_list = ["up", "right", "down", "left"]

        if (pygame.time.get_ticks() - timer) > 3000:
            timer = pygame.time.get_ticks()
            random_rotate = random.randrange(0, 3)
            if random_rotate == 0:
                level = rotate_map(level)
                rotate([player])
                rotate([enemy])
                rotate(scores)
                rotate_end(end_rect)
                rotate_pointer(p)
                n += 1
            if random_rotate == 1:
                level = rotate_map(rotate_map(level))
                rotate(rotate([player]))
                rotate(rotate([enemy]))
                rotate(rotate(scores))
                rotate_end(rotate_end(end_rect))
                rotate_pointer(rotate_pointer(p))
                n += 2
            if random_rotate == 2:
                level = rotate_map(rotate_map(rotate_map(level)))
                rotate(rotate(rotate([player])))
                rotate(rotate(rotate([enemy])))
                rotate(rotate(rotate(scores)))
                rotate_end(rotate_end(rotate_end(end_rect)))
                rotate_pointer(rotate_pointer(rotate_pointer(p)))
                n += 3
            if n >= 4:
                n = n % 4
            angle = angle_list[n]
            make_walls()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
            if e.type == pygame.K_ESCAPE:
                pause = True


        key = pygame.key.get_pressed()
        if angle == "up":
            x = 2
            y = 0
        elif angle == "left":
            x = 0
            y = -2
        elif angle == "right":
            x = 0
            y = 2
        elif angle == "down":
            x = -2
            y = 0

        # player 1
        if key[pygame.K_LEFT]:
            player.move(-x, -y)
        if key[pygame.K_RIGHT]:
            player.move(x, y)
        if key[pygame.K_UP]:
            player.move(y, -x)
        if key[pygame.K_DOWN]:
            player.move(-y, x)

        # player 2
        if key[pygame.K_a]:
            enemy.move(-x, -y)
        if key[pygame.K_d]:
            enemy.move(x, y)
        if key[pygame.K_w]:
            enemy.move(y, -x)
        if key[pygame.K_s]:
            enemy.move(-y, x)

        if player.rect.colliderect(end_rect):
            main_score = calculate_score()
            show_score(textX, textY, main_score)
            pygame.display.flip()
            pygame.time.wait(2000)
            return True

        if enemy.rect.colliderect(end_rect):
            text = font.render("GAME OVER!", True, (255, 255, 255))
            screen.blit(text, (10, 10))
            pygame.display.flip()
            pygame.time.wait(2000)
            return False

        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        for wall in walls:
            pygame.draw.rect(screen, (255, 255, 255), wall.rect)
        for score in scores:
            if score.enable:
                pygame.draw.rect(screen, (255, 255, 255), score.rect)
        screen.blit(fish, end_rect, )
        screen.blit(o_penguin, player.rect, )
        screen.blit(b_penguin, enemy.rect, )
        pygame.draw.polygon(screen, (250, 140, 80), [[p[0], p[1]], [p[2], p[3]], [p[4], p[5]]])
        pygame.display.flip()

        clock.tick(360)


i = -1
while -2 < i < 4:
    i += 1
    if i > 2:
        screen_size = [536, 536]
    a = Game(i)
    if a:
        continue
    b = Game(i)
    if b:
        continue
    i -= 2

pygame.quit()
