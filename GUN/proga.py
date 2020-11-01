from random import randrange as rnd, choice
import math
import pygame
from pygame.draw import *

pygame.init()
sc = pygame.display.set_mode((800, 600))

WHITE = (255,255,255)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS=[RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, ]

class ball():
    def __init__(self, x=40, y=570):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 100
        self.vy = 100
        self.power = 1
        self.color = COLORS[rnd(0,5)]
        #self.id = pygame.draw.ellipse(sc, self.color, (self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r))
        self.live = 30

    def draw(self):
        pygame.draw.circle(sc, self.color, (int(self.x), int(self.y)), self.r)

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if(not (self.y>=580 and self.vy<=4 and self.vx<=1)):
            self.x += self.vx
            self.y -= self.vy
            self.vy -= 2
            if(self.x>=790 and self.vx>0 or self.x<=10 and self.vx<0):
                self.vx *= -0.7
                self.vy *= 0.9
            if (self.y>=580 and self.vy<0 or self.y<=10 and self.vy>0):
                self.vy *= -0.7
                self.vx *= 0.9
        else:
            self.power = 0
        self.draw()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        if self.power and math.sqrt((self.x-obj.x)**2+(self.y-obj.y)**2)<=self.r+obj.r:
            return True
            #self.power = 0
        else:
            return False


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color=BLACK

    def draw(self):
        pygame.draw.line(sc, self.color, [20, 570],
                         [int(20 + max(self.f2_power, 20) * math.cos(self.an)),
                          int(570 + max(self.f2_power, 20) * math.sin(self.an))], 7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        x = event.pos[0]
        y = event.pos[1]
        self.an = math.atan((y-new_ball.y) / (x-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if not event==0 and event.type==pygame.MOUSEMOTION:
            x=event.pos[0]
            y=event.pos[1]
            if x != 20:
                self.an = math.atan((y-570) / (x-20))
            else:
                self.an=3.1415926535/2
        if self.f2_on:
            self.color=RED
        else:
            self.color=BLACK

        self.draw()

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color=RED
        else:
            self.color=BLACK


class target():
    def __init__(self):
        self.points = 0
        self.live = 1
        self.new_target()
        self.vx = rnd(-10,10)
        self.vy = rnd(-10,10)

    def draw(self):
        pygame.draw.circle(sc, RED, (int(self.x), int(self.y)), self.r)

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(2, 50)
        self.color = RED
        self.draw()

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if(self.x>=790 and self.vx>0 or self.x<=10 and self.vx<0):
            self.vx *= -1
        if (self.y>=580 and self.vy<0 or self.y<=10 and self.vy>0):
            self.vy *= -1
        self.draw()

def draw_score():
    global score
    font = pygame.font.Font(None, 100)
    text = font.render(str(score), True, BLACK)
    textpos = (25, 25)
    sc.blit(text, textpos)



t1 = target()
t2 = target()

g1 = gun()
bullet = 0
score = 0
balls = []


def new_game(event=''):
    global gun, t1, balls, bullet
    sc.fill(WHITE)

    t1.new_target()
    t2.new_target()
    bullet = 0
    balls = []

    t1.live = 1
    t2.live = 1
    finished = False
    pygame.display.update()
    clock = pygame.time.Clock()
    FPS = 30

    while (t1.live or t2.live) and not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                g1.fire2_start(event)
            if event.type == pygame.MOUSEBUTTONUP:
                g1.fire2_end(event)
            g1.targetting(event)

        for b in balls:
            b.move()
            for t in (t1,t2):
                if b.hittest(t) and t.live:
                    t.live = 0
                    #t1.hit()
            if t1.live+t2.live == 0:
                global score
                score+=1
                sc.fill(WHITE)
                font = pygame.font.Font(None, 40)
                text = font.render('Вы уничтожили цели за ' + str(bullet) + ' выстрелов', True, BLACK)
                textpos = (150, 300)
                sc.blit(text, textpos)
                pygame.display.update()
                clock.tick(0.5)
                break;

        for t in (t1, t2):
            if t.live==1:
                t.move()
        draw_score()
        g1.targetting()
        pygame.display.update()
        sc.fill(WHITE)
        g1.power_up()

    new_game()





new_game()



#mainloop()
