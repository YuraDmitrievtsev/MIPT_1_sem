import pygame
from pygame.draw import *
from random import randint

RESULT_ = 0
pygame.init()

FPS = 10
screen = pygame.display.set_mode((1200, 900))

GOLD = (255, 215, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
BAD_COLOR=(1,2,3)

class Ball(object):
    def __init__(self, position=[0,0], speed=[0,0],  radius=0, color=(0,0,0), deathtime=0):
        self.position = position
        self.speed=speed
        self.radius = radius
        self.color=color
        self.deathtime = deathtime
balls=[]
Snitches=[]


def new_ball(birthtime):
    '''рисует новый шарик '''
    deathtime = birthtime + randint(100,300)
    x = randint(100, 1100)
    y = randint(100, 900)
    vx = randint(-10, 10)
    vy = randint(-10, 10)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]

    balls.append(Ball([x,y],[vx,vy],r, color,deathtime))
    circle(screen, color, (x, y), r)

def new_Snitch(birthtime):
    deathtime = birthtime + 5000
    x = randint(50, 1150)
    y = randint(50, 950)
    vx = randint(-100, 100)
    vy = randint(-100, 100)
    #vx=0
    #vy=0
    r = 30
    color = GOLD

    Snitches.append(Ball([x, y], [vx, vy], r, color, deathtime))
    circle(screen, YELLOW, (x, y), r+5)
    circle(screen, color, (x, y), r-5)
    circle(screen, BLACK, (x, y), 5)

def update():
    screen.fill(BLACK)
    for i in balls:
        if (i.position[0] + i.radius >= 1200 or i.position[0] - i.radius <= 0):
            i.speed[0] *= (-1)
        if (i.position[1] + i.radius >=  900 or i.position[1] - i.radius <= 0):
            i.speed[1] *= (-1)
        i.position[0]+=i.speed[0]
        i.position[1]+=i.speed[1]
        x=i.position[0]
        y=i.position[1]
        r=i.radius
        color=i.color
        circle(screen, color, (x, y), r)

    for i in Snitches:
        if (i.position[0] + i.radius >= 1200 or i.position[0] - i.radius <= 0):
            i.speed[0] *= (-1)
        if (i.position[1] + i.radius >=  900 or i.position[1] - i.radius <= 0):
            i.speed[1] *= (-1)
        i.position[0]+=i.speed[0]
        i.position[1]+=i.speed[1]
        x=i.position[0]
        y=i.position[1]
        r=i.radius
        color=i.color
        circle(screen, YELLOW, (x, y), r + 5)
        circle(screen, color, (x, y), r)
        circle(screen, BLACK, (x, y), 5)

    font = pygame.font.Font(None, 100)
    text = font.render(str(RESULT_), True, BLACK)
    pygame.draw.polygon(screen, RED, [[0, 0], [0, 100], [200, 100], [200, 0]])
    textpos = (25, 25)
    screen.blit(text, textpos)

def death(i):
    x = i.position[0]
    y = i.position[1]
    r = i.radius
    circle(screen, BLACK, (x, y), r)
    balls.remove(i)
    update()

def sn_death(i):
    x = i.position[0]
    y = i.position[1]
    r = i.radius
    circle(screen, BLACK, (x, y), r+5)
    Snitches.remove(i)
    update()

def kill_the_ball(i):
    global RESULT_
    RESULT_+=1
    print("SHOT!!!")
    death(i)

def kill_them_all():
    print("BOOOOM!!!!!")
    for i in balls:
        global RESULT_
        RESULT_ += 1
        death(i)

def click(event):
    x=event.pos[0]
    y=event.pos[1]
    print('Click!')
    for i in balls:
        x0=i.position[0]
        y0=i.position[1]
        r0=i.radius
        if((x-x0)**2+(y-y0)**2<=r0**2):
            kill_the_ball(i)
    for i in Snitches:
        x0=i.position[0]
        y0=i.position[1]
        r0=i.radius+20
        if((x-x0)**2+(y-y0)**2<=r0**2):
            sn_death(i)
            kill_them_all()
            break

def cleaning(time):
    for i in balls:
        if(time>=i.deathtime):
            death(i)
    for i in Snitches:
        if (time >= i.deathtime):
            sn_death(i)
    update()

pygame.display.update()
clock = pygame.time.Clock()
finished = False


TIME = 0
while not finished:
    clock.tick(FPS)
    TIME += FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    new_ball(TIME)
    Sn=randint(0,100)
    if(Sn==100):
        new_Snitch(TIME)
    cleaning(TIME)
    pygame.display.update()

pygame.quit()

print(RESULT_)