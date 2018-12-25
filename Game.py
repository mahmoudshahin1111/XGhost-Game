from Ghost import *
from Enemy import *
from Bullet import *
from Constants import *



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_NAME)

        self.image = pygame.image.load("gothic-castle-preview.png")

        self.rect = self.image.get_rect()
        self.backGround = pygame.display.set_mode([self.rect.width, self.rect.height])
        self.guns = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.run = True
        self.gameOver = False
        self.textGame = pygame.Surface([0, 0])
        self.end_txt = TXT_WINNER
        self. levels = 2
        self.score = 0


        self.initGun()
        self.createEnemy()
        self.draw()

    def initGun(self):
        gun = Gun(self.rect.copy())
        gun.add(self.guns)

    def createEnemy(self):
        for i in range(1,2):
            rand = random.randint(self.rect.width-400,self.rect.width-100)
            enemy = Enemy(self.rect.copy(),rand+50,(i*10)+(rand/10))
            enemy.add(self.enemys)

    def checkIfBulletOut(self,bulletOwner):
        for owner in bulletOwner:
            for bullet in owner.bullets:
                if not self.rect.contains(bullet.rect):
                    bullet.kill()
    def endGame(self):
        font = pygame.font.SysFont(ARIAL,SIZE_2)
        self.textGame = font.render(self.end_txt, False, C_RED)

    def isPlayerDead(self):
        #check if enemys bullet collide with gun
        for enemy in self.enemys:
            self.gameOver = pygame.sprite.groupcollide(self.guns,enemy.bullets,False,True)
            if self.gameOver:
                self.end_txt = TXT_GAME_OVER +" You Killed : "+ str(self.score)
                self.endGame()
                return

    def isEnemyKilled(self):
        gun = self.guns.sprites()[0]
        before = len(self.enemys)
        pygame.sprite.groupcollide(gun.bullets,self.enemys,True,True)
        after = len(self.enemys)
        self.score += before - after
        if len(self.enemys) == 0:
            self.end_txt = TXT_WINNER +" You Killed : "+ str(self.score)
            self.endGame()
            self.gameOver = True

    def draw(self):
        while self.run:
            gun = self.guns.sprites()[0]
            pygame.time.delay(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                else:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_DOWN]:
                        gun.down = True
                    elif keys[pygame.K_UP]:
                        gun.up = True
                    elif keys[pygame.K_SPACE]:
                        gun.fire = True
                    else:
                        gun.up = False
                        gun.down = False
                        gun.right = False
                        gun.left = False

            self.backGround.blit(self.image,self.image.get_rect())
            if not self.gameOver:
                self.isPlayerDead()
                self.isEnemyKilled()
                self.checkIfBulletOut(self.enemys)
                self.checkIfBulletOut(self.guns)

                #update groups
                self.guns.update()
                self.enemys.update()

                #draw bullets
                self.guns.draw(self.backGround)
                for gun in self.guns:
                    gun.bullets.draw(self.backGround)
                for enemy in self.enemys:
                    self.backGround.blit(enemy.image,enemy.rect)
                    enemy.bullets.draw(self.backGround)

                #RANDOM FOR GHOSTS
                addNEnemyC = random.randint(1, 30)
                if addNEnemyC == 3 :
                    self.createEnemy()
                font = pygame.font.SysFont(ARIAL, SIZE_2)
                txt_score = font.render(str(self.score), True, C_RED)
                self.backGround.blit(txt_score,(300,0))

            else:
                self.backGround.blit(self.textGame, (300, 150))
            pygame.display.flip()