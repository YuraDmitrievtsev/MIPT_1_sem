from random import randrange as rnd, choice
import math
import pygame
from pygame.draw import *

pygame.init()
WIDTH = 800
HEIGHT = 600
gameover=False
sc = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, ]


def Length(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def draw_score():
    global score
    font = pygame.font.Font(None, 100)
    text = font.render(str(score), True, BLACK)
    textpos = (25, 25)
    sc.blit(text, textpos)

def GAME_OVER():
    sc.fill(BLACK)
    font = pygame.font.Font(None, 100)
    text = font.render("GAME OVER", True, RED)
    textpos = (200,200)
    sc.blit(text, textpos)
    global gameover
    gameover=True
    pygame.display.update()

class MovingObject():
    def __init__(self, x, y, r, vx=0, vy=0, mass=0):
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.color = COLORS[rnd(0, 5)]

    def draw(self):
        pygame.draw.circle(sc, self.color, (int(self.x), int(self.y)), self.r)

    def move(self, attenuation=0, friction=0):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.mass
        if (self.x >= WIDTH - self.r and self.vx > 0 or self.x <= self.r and self.vx < 0):
            self.vx *= -attenuation
            self.vy *= friction
        if (self.y >= HEIGHT - self.r and self.vy > 0 or self.y <= self.r and self.vy < 0):
            self.vy *= -attenuation
            self.vx *= friction
        self.draw()


class ball(MovingObject):
    def __init__(self, x=40, y=570, r=10, vx=0, vy=0, mass=2, power=1):
        MovingObject.__init__(self, x, y, r, vx, vy, mass)
        self.power = power

    def move(self, attenuation=0.7, friction=0.9):
        if (not (self.y >= HEIGHT - self.r and abs(self.vy) <= 5 and abs(self.vx) <= 1) and self.power):
            MovingObject.move(self, attenuation, friction)
        else:
            self.power = 0

    def hittest(self, obj):
        if self.power and obj.power == 1 and Length(self.x,self.y,obj.x,obj.y) <= self.r + obj.r:
            self.power = 0
            return True
        else:
            return False


class pellet(ball):
    def __init__(self, x=40, y=570, r=3, vx=0, vy=0, mass=1, power=1):
        ball.__init__(self, x, y, r, vx, vy, mass, power)

    def move(self):
        if (self.vx == 0 and self.vy == 0):
            self.power = 0
        else:
            MovingObject.move(self)


class landmine(ball):
    def __init__(self, x=40, y=570, r=20, vx=0, vy=0, mass=7, power=1):
        ball.__init__(self, x, y, r, vx, vy, mass, power)

    def boom(self):
        global balls
        self.power = 0
        for an in range(0, 10):
            new_ball = pellet()
            new_ball.x = self.x
            new_ball.y = self.y
            pi = 3.14159265359
            new_ball.vx = self.vx + 5 * math.cos(an * pi / 5)
            new_ball.vy = self.vy + 5 * math.sin(an * pi / 5)
            balls += [new_ball]

    def move(self):
        if (self.power and
                (  self.x >= WIDTH-self.r and self.vx < 0
                or self.x <= self.r and self.vx > 0
                or self.y >= HEIGHT-self.r and self.vy < 0
                or self.y <= self.r and self.vy > 0)):
            self.boom()
            self.power=0
        ball.move(self,1,1)


class gun(MovingObject):
    def __init__(self, x=70, y=570, r=0, vx=0, vy=0, mass=0):
        MovingObject.__init__(self, x, y, r, vx, vy, mass)
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = BLACK
        self.mode = 0
        self.acceleration=0

    def draw(self):
        pygame.draw.line(sc, self.color, [int(self.x), int(self.y)],
                         [int(self.x + max(self.f2_power, 20) * math.cos(self.an)),
                          int(self.y + max(self.f2_power, 20) * math.sin(self.an))], 7)
        pygame.draw.line(sc, BLACK, [int(self.x-10), int(self.y)], [int(self.x+10), int(self.y)],10)
        pygame.draw.line(sc, BLACK, [int(self.x-50), int(self.y+10)], [int(self.x+50), int(self.y+10)], 10)

    def move(self, friction=0.3):
        self.vx+=self.acceleration*0.6
        if abs(self.vx)<0.1 and self.acceleration==0:
            self.vx=0
        if self.x+50>=WIDTH or self.x-50<=0:
            self.vx*=-1
        if self.vx > 0:
            self.vx -= friction
        elif self.vx < 0:
            self.vx += friction
        self.x+=self.vx
        MovingObject.move(self)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        global balls, bullet
        bullet += 1
        if self.mode <= 1:
            if self.mode == 0:
                new_ball = ball(self.x,self.y)
            if self.mode == 1:
                new_ball = landmine(self.x,self.y)

            x = event.pos[0]
            y = event.pos[1]
            self.an = -math.acos((x - self.x) / Length(x, y, self.x, self.y))
            new_ball.vx = self.f2_power * math.cos(self.an) + self.vx
            new_ball.vy = self.f2_power * math.sin(self.an)
            balls += [new_ball]
            self.f2_on = 0
            self.f2_power = 10
        elif self.mode == 2:
            for i in range(self.f2_power):
                new_ball = pellet()

                new_ball.color=BLUE
                new_ball.mass=0
                x = event.pos[0]
                y = event.pos[1]
                self.an = -math.acos((x - self.x) / Length(x, y, self.x, self.y))
                new_ball.x=self.x-7*i*math.cos(self.an)
                new_ball.y=self.y-7*i*math.sin(self.an)
                new_ball.vx = self.f2_power * math.cos(self.an) + self.vx
                new_ball.vy = self.f2_power * math.sin(self.an)
                balls += [new_ball]
            self.f2_on = 0
            self.f2_power = 10


    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if not event == 0 and event.type == pygame.MOUSEMOTION:
            x = event.pos[0]
            y = event.pos[1]
            if x != self.x:
                self.an = -math.acos((x - self.x)/Length(x,y,self.x,self.y))
                #self.an = math.atan((y - self.y) / (x - self.x))
            else:
                self.an = 3.1415926535 / 2
        if self.f2_on:
            self.color = RED
        else:
            self.color = BLACK

        #self.draw()

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = BLACK


class bomb(pellet):
    def __init__(self, x=40, y=570, r=15, vx=0, vy=0, mass=0.5, power=1):
        ball.__init__(self, x, y, r, vx, vy, mass, power)
        self.color=BLACK

    def move(self):
        if self.y>=HEIGHT-self.r-1:
            self.power=0
        ball.move(self)

    def hit(self, obj):
        if self.power and abs(self.y-obj.y)<self.r and self.x<obj.x+50 and self. x>obj.x-50:
            return True
        else:
            return False


class target(bomb):
    def __init__(self, mass=0):
        self.x=rnd(600, 780)
        self.y=rnd(300, 550)
        self.r=rnd(2, 50)
        self.vx=rnd(-10, 10)
        self.vy=rnd(-10, 10)
        self.mass=mass
        self.color = RED
        self.power = 1

    def move(self):
        MovingObject.move(self, 1, 1)


class aircraft(MovingObject):
    def __init__(self, vy=0, mass=0, color=BLACK, live=1):
        self.x = rnd(20, 780)
        self.y = rnd(100, 400)
        self.r = 20
        self.orr=rnd(0,2)
        if self.orr==0:
            self.orr=-1
        self.vx = rnd(10,20)*self.orr
        self.vy = vy
        self.mass = mass
        self.color = color
        self.power = 1

    def draw(self):
        if self.orr == 1:
            pygame.draw.polygon(sc, self.color, [[int(self.x+30),int(self.y)]
                                            ,[int(self.x-30),int(self.y+10)]
                                            ,[int(self.x-30),int(self.y-10)]])
        if self.orr == -1:
            pygame.draw.polygon(sc, self.color, [[int(self.x - 30), int(self.y)]
                , [int(self.x + 30), int(self.y + 10)]
                , [int(self.x + 30), int(self.y - 10)]])

    def bam(self):
        global bombs
        new_bomb = bomb(self.x,self.y,15,self.vx)
        bombs+=[new_bomb]

    def move(self):
        self.x+=self.vx
        if not rnd(0,100):
            self.bam()
        if (self.x >= WIDTH and self.orr == 1):
            self.x = 0
        if (self.x <= 0 and self.orr == -1):
            self.x = WIDTH
        self.draw()



g1 = gun()
bullet = 0
score = 0
balls = []
bombs=[]


def new_game(event=''):
    global gun, t1, balls, bullet, gameover, bombs
    sc.fill(WHITE)

    bombs = []
    targets = []
    for i in range(5):
        targets += [target()]
        targets += [aircraft()]
    bullet = 0
    balls = []
    lives = 10
    finished = False
    pygame.display.update()
    clock = pygame.time.Clock()
    FPS = 30

    while lives and not finished and not gameover:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                g1.fire2_start(event)
            if event.type == pygame.MOUSEBUTTONUP:
                g1.fire2_end(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    g1.mode = 0
                if event.key == pygame.K_2:
                    g1.mode = 1
                if event.key == pygame.K_3:
                    g1.mode = 2
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    g1.acceleration=1
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    g1.acceleration=-1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT \
                        or event.key == pygame.K_LEFT\
                        or event.key == pygame.K_a \
                        or event.key == pygame.K_d:
                    g1.acceleration=0

            g1.targetting(event)

        for b in balls:
            b.move()
            for t in targets:
                if b.hittest(t) and t.power:
                    t.power = 0
                    lives-=1
                    if b.mass == 7:
                        b.boom()
            for bomb in bombs:
                if b.hittest(bomb) and bomb.power:
                    bomb.power=0
                    if b.mass == 7:
                        b.boom()

            if lives == 0:
                global score
                score += 1
                sc.fill(WHITE)
                font = pygame.font.Font(None, 40)
                text = font.render('Вы уничтожили цели за ' + str(bullet) + ' выстрелов', True, BLACK)
                textpos = (150, 300)
                sc.blit(text, textpos)
                pygame.display.update()
                clock.tick(0.5)
                break


        for bomb in bombs:
            bomb.move()
            if bomb.hit(g1):
                GAME_OVER()
                gameover=True
                finished-True
                clock.tick(0.3)
                return

        for t in targets:
            if t.power == 1:
                t.move()
            if t.color==RED and t.hit(g1):
                GAME_OVER()
                gameover=True
                finished-True
                clock.tick(0.3)
                return

        draw_score()
        g1.targetting()
        g1.move()
        pygame.display.update()
        sc.fill(WHITE)
        g1.power_up()

    if not finished and not gameover:
        new_game()


new_game()
