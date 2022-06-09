
from random import random
import pygame
import random

pygame.init()
running = True
pygame.display.set_caption("Snake")
WIN_SIZE = 600
screen = pygame.display.set_mode((WIN_SIZE,WIN_SIZE))
BACK_GROUND = (0,0,0)
screen.fill(BACK_GROUND)
SQR_SIZE = 10
FOOD_SIZE = 20
speed = SQR_SIZE

def lost():
    font = pygame.font.SysFont("arial", 64)
    text = font.render("YOU LOST", False, "red")
    textRect = text.get_rect()
    textRect.center = (WIN_SIZE / 2, WIN_SIZE / 2)
    screen.blit(text, textRect)
    pygame.display.update()
    pygame.time.delay(1000)
    quit()

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([FOOD_SIZE,FOOD_SIZE])
        self.image.fill("green")
        self.image.set_colorkey(BACK_GROUND)

        self.rect = self.image.get_rect()
        self.rect.y = (int(random.randint(0,570)/FOOD_SIZE))*FOOD_SIZE
        self.rect.x = (int(random.randint(0,570)/FOOD_SIZE))*FOOD_SIZE
        pygame.draw.rect(screen, "green",pygame.Rect(self.rect.x, self.rect.y, FOOD_SIZE, FOOD_SIZE))

dir = ""
food = Food()
#class na vytvorenie bloku hada

class Snake(pygame.sprite.Sprite):

    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface([SQR_SIZE, SQR_SIZE])
        self.image.fill(color)
        self.image.set_colorkey(BACK_GROUND)
        pygame.draw.rect(screen,color,pygame.Rect(WIN_SIZE/2-SQR_SIZE, WIN_SIZE/2-SQR_SIZE, SQR_SIZE, SQR_SIZE))
        self.rect = self.image.get_rect()

    def move(self):
        if dir == "UP":
            self.rect.y-=speed
        if dir == "RIGHT":
            self.rect.x+=speed
        if dir == "LEFT":
            self.rect.x-=speed
        if dir == "DOWN":
            self.rect.y+=speed

#vytvorime spritelist, zoznam Snake objektov, pociatok dame do stredu okna
fruitlist = pygame.sprite.Group()
fruitlist.add(food)
spritelist = pygame.sprite.Group()
snake_len = 1
snake = [Snake("red") for i in range(1)]

for j in range(snake_len):    
    snake[j].rect.x = WIN_SIZE/2 - SQR_SIZE
    snake[j].rect.y = WIN_SIZE/2 - SQR_SIZE

flag = False
#do spritelistu pridame prvy objekt
for j in range(snake_len):
    spritelist.add(snake[j])

#game loop
while running:
    pygame.time.delay(40)
    for event in pygame.event.get(): 
        #ked stlacime quit button, skoncime 
        if event.type == pygame.QUIT:  
            running = False

        #ked stlacime nejaku klavesu, tak zmenime dir
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and dir != "RIGHT":
                dir = "LEFT"
            if event.key == pygame.K_w and dir != "DOWN":
                dir = "UP"
            if event.key == pygame.K_s and dir != "UP":
                dir = "DOWN"
            if event.key == pygame.K_d and dir != "LEFT":
                dir = "RIGHT"

    #ak mame koliziu hlavy a jedla
    if pygame.Rect.colliderect(snake[snake_len-1].rect,food.rect):
        fruitlist.empty()
        flag = True

    #skontrolujeme ci had nenarazil sam do seba
    for i in range(snake_len-1):
        if(pygame.Rect.colliderect(snake[snake_len-1].rect,snake[i].rect)):
            lost()

    #ci nie je mimo okna
    if snake[snake_len-1].rect.x > (WIN_SIZE - SQR_SIZE) or snake[snake_len-1].rect.y > (WIN_SIZE - SQR_SIZE) or snake[snake_len-1].rect.x < 0 or snake[snake_len-1].rect.y < 0:
        lost()
    #vytvorime novu hlavu, priradime jej poziciu predoslej hlavy a pridame do listu snake

    toadd = Snake("red")
    toadd.rect.y = snake[snake_len-1].rect.y
    toadd.rect.x = snake[snake_len-1].rect.x
    snake.append(toadd)
    #ci chceme odstranit koniec hada - zalezi, ci spapal jedlo

    if not flag:
        snake.pop(0)
    else:
        food = Food()
        fruitlist.add(food)
        snake_len+=1
        flag = False
    #pohneme hlavou
    snake[snake_len-1].move()

    #vyprazdnime spritelist a znova ho naplnime "novym" hadom
    spritelist.empty()
    for j in range(snake_len):
        spritelist.add(snake[j])
    spritelist.update()
    screen.fill(BACK_GROUND)
    spritelist.draw(screen)
    fruitlist.draw(screen)
    pygame.display.update()
    
pygame.quit()




