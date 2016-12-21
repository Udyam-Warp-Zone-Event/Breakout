import pygame
import random
import math
from pygame import *


scr_size = (width,height) = (600,400)
FPS = 50
black = (0,0,0)
white = (255,255,255)
__colors__ = [blue,red,green,yellow,orange,purple,pink] = [(50,50,255),(204,0,0),(0,153,0),(255,255,0),(255,128,0),(102,0,102),(255,51,153)]

clock = pygame.time.Clock()
screen = pygame.display.set_mode(scr_size)

pygame.display.set_caption('Breakout')

class Ball():
    def __init__(self,x,y,size,color,movement=[0,0]):
        self.image = pygame.Surface((size,size),SRCALPHA,32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image,color,(int(self.rect.width/2),int(self.rect.height/2)),int(size/2))
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 2
        self.maxspeed = 4
        self.score = 0
        self.movement = movement
        self.isLaunched = False

    def checkbounds(self):
        if self.isLaunched == True:
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > height:
                self.rect.bottom = height
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > width:
                self.rect.right = width
        else:
            if self.rect.centerx > width - 40:
                self.rect.centerx = width - 40

            if self.rect.centerx < 40:
                self.rect.centerx = 40

    def update(self):
        if self.isLaunched == True:
            if self.rect.top == 0 or self.rect.bottom == height:
                self.movement[1] = -1*self.movement[1]
            if self.rect.left == 0 or self.rect.right == width:
                self.movement[0] = -1*self.movement[0]

            if self.movement[0] >= self.maxspeed or self.movement[0] <= -1*self.maxspeed:
                self.movement[0] = (math.fabs(self.movement[0])/self.movement[0])*self.maxspeed

            self.rect = self.rect.move(self.movement)
            self.checkbounds()
        else:
            self.rect = self.rect.move(self.movement)
            self.checkbounds()

    def draw(self):
        screen.blit(self.image,self.rect)

class Brick(pygame.sprite.Sprite):
    def __init__(self,x,y,sizex,sizey,color):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.Surface((sizex,sizey),SRCALPHA,32)
        self.rect = self.image.get_rect()

        self.rect.left = x
        self.rect.top = y

        self.image.fill(color)

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        pass

class Paddle():
    def __init__(self, x, y, sizex, sizey, color):
        self.image = pygame.Surface((sizex, sizey), SRCALPHA, 32)
        self.rect = self.image.get_rect()

        self.rect.left = x
        self.rect.top = y

        self.image.fill(color)

        self.movement = [0,0]
        self.speed = 8

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        self.checkbounds()

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width



def main():
    gameOver = False
    bricks = pygame.sprite.Group()

    Brick.containers = bricks

    for i in range(0,9):
        for j in range(0,5):
            Brick(16 + 10*(j%2) + i*64,30 + j*20,int(width*54/600),int(height*10/400),__colors__[random.randrange(0,7)])

    myPaddle = Paddle(width/2,height - height/10,80,10,white)
    myBall = Ball(myPaddle.rect.centerx,myPaddle.rect.centery - myPaddle.rect.height/2 - 6,12,__colors__[2])

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    myPaddle.movement[0] = -1*myPaddle.speed
                    if myBall.isLaunched == False:
                        myBall.movement[0] = -1*myPaddle.speed

                if event.key == pygame.K_RIGHT:
                    myPaddle.movement[0] = myPaddle.speed
                    if myBall.isLaunched == False:
                        myBall.movement[0] = myPaddle.speed

                if event.key == pygame.K_SPACE:
                    if myBall.isLaunched == False:
                        myBall.isLaunched = True
                        myBall.movement = [myBall.speed*(random.randrange(0,3,2) - 1),-1*myBall.speed]

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    myPaddle.movement[0] = 0
                    if myBall.isLaunched == False:
                        myBall.movement[0] = 0

        for brick in bricks:
            if pygame.sprite.collide_mask(myBall,brick):
                #print 'chutzpah'
                if myBall.rect.top <= brick.rect.bottom or myBall.rect.bottom >= brick.rect.top:
                    myBall.movement[1] = -1*myBall.movement[1]

                if myBall.rect.left >= brick.rect.right or myBall.rect.right <= brick.rect.left:
                    myBall.movement[0] = -1*myBall.movement[0]
                brick.kill()

        if pygame.sprite.collide_mask(myBall,myPaddle):
            if myBall.rect.bottom >= myPaddle.rect.top:
                myBall.movement[1] = -1*myBall.movement[1]
                myBall.movement[0] = myBall.movement[0] - myPaddle.movement[0]


        myPaddle.update()
        bricks.update()
        myBall.update()

        screen.fill(black)
        myPaddle.draw()
        myBall.draw()
        bricks.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

main()
