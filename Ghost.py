import Constants
import pygame
from SpriteSheet import *
from Bullet import *

class Gun(pygame.sprite.Sprite):

    def __init__(self, map_rect):
        pygame.sprite.Sprite.__init__(self)
        self.spreedSheet = spritesheet(PLAYER_IMAGE)
        self.animatCounter = 0
        self.images = [
            self.spreedSheet.image_at((20, 20, 30, 50), -1),
            self.spreedSheet.image_at((85, 20, 30, 50), -1),
            self.spreedSheet.image_at((150, 20, 30, 50), -1),
            self.spreedSheet.image_at((215, 20, 30, 50), -1),
        ]
        self.image = pygame.Surface([25,40])
        self.rect = self.image.get_rect()
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.acceleration_y = PLAYER_ACCELERATION_Y
        self.acceleration_x = PLAYER_ACCELERATION_X
        self.x_change = 0
        self.y_change = 0
        self.max_speed = 4
        self.fire = False
        self.isDead = False
        self.bullets = pygame.sprite.Group()
        self.max_bullets = PLAYER_MAX_BULLETS
        self.mapRect = map_rect
        self.time = 0
    def animating(self):
        if self.time%10 == 0:

            if self.animatCounter < len(self.images)-1:
                self.image = self.images[abs(self.animatCounter)]
                self.animatCounter += 1
            else:
                self.animatCounter *= -1
        self.time += 1

    def move(self):
        self.acceleration_x = PLAYER_ACCELERATION_X
        self.acceleration_y = PLAYER_ACCELERATION_Y
        if self.rect.top < 0 or self.rect.bottom > self.mapRect.height:
            self.up = False
            self.down = False
            self.y_change *= -1

        elif self.up:
            if abs(self.y_change) >= self.max_speed:
                self.acceleration_y = 0
            self.y_change -= self.acceleration_y

        elif self.down:
            if abs(self.y_change) >= self.max_speed:
                self.acceleration_y = 0
            self.y_change += self.acceleration_y

        elif self.right:
            if abs(self.x_change) >= self.max_speed:
                self.acceleration_x = 0
            self.x_change += self.acceleration_x
        elif self.left:
            if abs(self.x_change) >= self.max_speed:
                self.acceleration_x = 0
            self.x_change -= self.acceleration_x
        elif self.fire:
            self.shoot()

        else:
            self.y_change *= .92
            self.x_change *= .92
        self.rect.move_ip(self.x_change, self.y_change)

    def shoot(self):
        if len(self.bullets.sprites()) < self.max_bullets:
            if self.fire:
                bullet = Bullet(self.rect)
                bullet.add(self.bullets)
        self.fire = False

    def update(self, *args):

        self.move()
        self.animating()
        self.bullets.update()
