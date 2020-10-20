import pygame
from pygame.draw import *
from random import randint

RESULT_ = 0
pygame.init()

FPS = 10
screen = pygame.display.set_mode((1200, 900))
gameover=False

WHITE = (255,255,255)
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

class Sign(object):
    def __init__(self, position=[0,0], name='', color=(0,0,0), deathtime=0):
        self.position = position
        self.name=name
        self.color = color
        self.deathtime = deathtime


balls=[]
Snitches=[]
deathdots=[]
signes=[]

def new_ball(birthtime): #Создание нового шарика
    deathtime = birthtime + randint(200,500)
    x = randint(100, 1100)
    y = randint(100, 900)
    vx = randint(-10, 10)
    vy = randint(-10, 10)
    r = randint(10, 50)
    color = COLORS[randint(0, 5)]

    balls.append(Ball([x,y],[vx,vy],r, color,deathtime))
    circle(screen, color, (x, y), r)

def new_Snitch(birthtime): #Создание нового снитча
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

def new_deathdot(birthtime): # новая смертельная точка
    deathtime = birthtime + 5000
    x = randint(50, 1190)
    y = randint(50, 990)
    vx = 0
    vy = 0
    r=10
    color = WHITE

    deathdots.append(Ball([x, y], [vx, vy], r, color, deathtime))
    circle(screen, color, (x, y), r)
    circle(screen, BLACK, (x, y), 5)

def draw(sign,x,y,birthtime):
    deathtime = birthtime + 5
    color=COLORS[randint(0, 5)]

    signes.append(Sign([x,y],sign,color,deathtime))

    font = pygame.font.Font(None, 100)
    text = font.render(sign, True, color)
    textpos = (x, y)
    screen.blit(text, textpos)

def update(): #Обновление
    screen.fill(BLACK)

    for i in deathdots:
        x = i.position[0]
        y = i.position[1]
        r = i.radius
        color = i.color
        circle(screen, color, (x, y), r)
        circle(screen, BLACK, (x, y), 5)

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

    for i in signes:
        x = i.position[0]
        y = i.position[1]
        color = i.color
        font = pygame.font.Font(None, 100)
        text = font.render(sign, True, color)
        textpos = (x, y)
        screen.blit(text, textpos)

    font = pygame.font.Font(None, 100)
    text = font.render(str(RESULT_), True, BLACK)
    pygame.draw.polygon(screen, RED, [[0, 0], [0, 100], [200, 100], [200, 0]])
    textpos = (25, 25)
    screen.blit(text, textpos)

def death(i): #смерть шарика
    x = i.position[0]
    y = i.position[1]
    r = i.radius
    circle(screen, BLACK, (x, y), r)
    balls.remove(i)
    #update()

def sn_death(i): #смерть снитча
    x = i.position[0]
    y = i.position[1]
    r = i.radius
    circle(screen, BLACK, (x, y), r+5)
    Snitches.remove(i)
    #update()

def dd_death(i): #смерть точки
    x = i.position[0]
    y = i.position[1]
    r = i.radius
    circle(screen, BLACK, (x, y), r)
    deathdots.remove(i)
    #update()

def kill_the_ball(i): #убить шарик
    global RESULT_
    RESULT_+=1
    print("SHOT!!!")
    death(i)

def kill_them_all(): #убить все шарики
    print("BOOOOM!!!!!")
    for i in balls:
        global RESULT_
        RESULT_ += 1
        death(i)

def GAME_OVER():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 100)
    text = font.render("GAME OVER", True, RED)
    textpos = (400,400)
    screen.blit(text, textpos)
    global gameover
    gameover=True
    pygame.display.update()

def click(event,time): #клик по экрану
    x=event.pos[0]
    y=event.pos[1]

    #draw('Click!',x,y,time)
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
    for i in deathdots:
        x0 = i.position[0]
        y0 = i.position[1]
        r0 = i.radius
        if ((x-x0)**2+(y-y0)**2<=r0**2):
            GAME_OVER()

def cleaning(time): #очистка поля
    for i in balls:
        if(time>=i.deathtime):
            death(i)
    for i in Snitches:
        if (time >= i.deathtime):
            sn_death(i)
    for i in deathdots:
        if (time >= i.deathtime):
            dd_death(i)

    update()



pygame.display.update()
clock = pygame.time.Clock()
finished = False


print("enter your name:")
name=input()
TIME = 0
while not finished:
    clock.tick(FPS)
    TIME += FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and not gameover:
            click(event,TIME)
    if not gameover:
        new_ball(TIME)
        if(randint(0,100)==0):
            new_Snitch(TIME)
        if (randint(0,30)==0):
            new_deathdot(TIME)
        cleaning(TIME)
        pygame.display.update()


pygame.quit()

table=[]
file = open('Results.txt','r')
for i in file.readlines():
    table.append(i.split(':'))
table.append([0,name,str(RESULT_),'\n'])
tables=sorted(table, key=lambda t: -int(t[2]))
print(tables)
file = open('Results.txt','w')
file.flush()
for i in range(len(tables)):
    file.write(str(i+1)+':'+tables[i][1]+':'+tables[i][2]+':\n')
print(name,':',RESULT_)

