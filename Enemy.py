import Constants
import pygame
import random
from SpriteSheet import *
from Bullet import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self,map_rect,x = 300,y = 100):
        pygame.sprite.Sprite.__init__(self)
        self.spriteSheet = spritesheet("fire-skull.png")
        self.images =[
            self.spriteSheet.image_at((010, 25, 80, 80), -1),
            self.spriteSheet.image_at((100, 20, 80, 80), -1),
            self.spriteSheet.image_at((190, 10, 80, 80), -1),
            self.spriteSheet.image_at((295, 25, 80, 80), -1),
            self.spriteSheet.image_at((390, 25, 80, 80), -1),
            self.spriteSheet.image_at((495, 30, 80, 80), -1),
            self.spriteSheet.image_at((580, 30, 80, 80), -1),
            self.spriteSheet.image_at((680, 25, 80, 80), -1),
        ]
        self.animatCounter = 0
        self.image = self.images[1]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.up = False
        self.down = True
        self.left = False
        self.y_change = ENEMY_Y_SPEED
        self.x_change = ENEMY_X_SPEED
        self.bullets = pygame.sprite.Group()
        self.max_Bullets = ENEMY_MAX_BULLETS

        self.mapRect = map_rect
        self.time = 0
    def animating(self):
        if self.time%10 == 0:

            if self.animatCounter < len(self.images)-1:
                self.image = self.images[abs(self.animatCounter)]
                self.image= pygame.transform.scale(self.image,(30,30))
                self.animatCounter += 1
            else:
                self.animatCounter *= -1
        self.time += 1
    def domoving(self):
        rand = random.randint(1,50)
        if rand == 25:
            self.shoot()
        elif rand == 1:
            self.left = True

        if self.rect.top < 0:
            self.down = True
            self.up = False
        elif self.rect.bottom > self.mapRect.height:
            self.down = False
            self.up = True

        if self.up:
            self.y_change = -ENEMY_Y_SPEED
        elif self.down:
            self.y_change = ENEMY_Y_SPEED
        if self.left:
            self.left = False
            self.x_change = -ENEMY_X_SPEED
        self.rect.move_ip(self.x_change,self.y_change)
        self.x_change = 0

    def shoot(self):
        if len(self.bullets.sprites()) < self.max_Bullets:
            bullet = Bullet(self.rect,True)
            bullet.add(self.bullets)

    def update(self, *args):
        self.animating()
        self.domoving()
        self.bullets.update()