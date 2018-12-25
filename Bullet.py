import pygame
from Constants import *
from SpriteSheet import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, gun_Position,left = False):
        pygame.sprite.Sprite.__init__(self)

        self.spriteSheet = spritesheet("fire-ball.png")
        self.images = [
            self.spriteSheet.image_at((1, 3, 18, 13), -1),
            self.spriteSheet.image_at((20, 3, 18, 13), -1),
            self.spriteSheet.image_at((40, 3, 18, 13), -1),
        ]
        self.animatCounter = 0
        self.image = self.images[1]
        self.rect = self.image.get_rect()
        self.rect.x = gun_Position.centerx + gun_Position.width
        self.rect.y = gun_Position.centery
        if left:
            self.acceleration_x = -0.3
        else:
            self.acceleration_x = 0.3

        self.x_change = 0
        self.max_speed = 3
        self.index = 0
        self.time = 0

    def animating(self):
        if self.time % 10 == 0:

            if self.animatCounter < len(self.images) - 1:
                self.image = self.images[abs(self.animatCounter)]
                self.image = pygame.transform.scale(self.image, (10, 10))
                self.animatCounter += 1
            else:
                self.animatCounter *= -1
        self.time += 1

    def move(self):
        if abs(self.x_change) >= self.max_speed:
            self.acceleration_x = 0
        self.x_change += self.acceleration_x
        self.rect.move_ip(self.x_change, 0)

    def update(self, *args):
        self.move()
        pass