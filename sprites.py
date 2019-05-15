import pygame
from settings import*
import sys, os
vec = pygame.math.Vector2
import random
from os import path


def collide_with_obs(sprite, group, direction):
    if direction == "x":
        # return a list containing all Sprites in a group
        # that intersect with another Sprite.
        rectHits = pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_rect)
        if rectHits:
            if rectHits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = rectHits[0].rect.left - sprite.rect.width/2
            if rectHits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = rectHits[0].rect.right + sprite.rect.width/2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x

    if direction == "y":
        # return a list containing all Sprites in a group
        # that intersect with another Sprite.
        rectHits = pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_rect)
        if rectHits:
            if rectHits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = rectHits[0].rect.top - sprite.rect.height/2
            if rectHits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = rectHits[0].rect.bottom + sprite.rect.height/2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.gameFolder = path.dirname(__file__)
        self.imgFolder = path.join(self.gameFolder, "LibRPG")
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load(path.join(self.imgFolder, player_front)).convert_alpha()
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.playerHealth = playerStat["CON"]
        self.playerSan = playerStat["SAN"]
        self.crazy = playerStat["CRAZY"]
        self.dir = vec(0, 0)
        self.lastshoot = 0
        self.lastcrazy = 0

    def get_keyPressed(self):
        keys = pygame.key.get_pressed()
        self.vel = vec(0, 0)
        if keys[pygame.K_LEFT]:
            self.vel = vec(-playerSpeed, 0)
            self.dir = vec(-1, 0)
            self.image = pygame.image.load(path.join(self.imgFolder, player_left)).convert_alpha()

        if keys[pygame.K_RIGHT]:
            self.vel = vec(playerSpeed, 0)
            self.player = player_right
            self.dir = vec(1, 0)
            self.image = pygame.image.load(path.join(self.imgFolder, player_right)).convert_alpha()

        if keys[pygame.K_UP]:
            self.vel = vec(0, -playerSpeed)
            self.player = player_back
            self.dir = vec(0, -1)
            self.image = pygame.image.load(path.join(self.imgFolder, player_back)).convert_alpha()


        if keys[pygame.K_DOWN]:
            self.vel = vec(0, playerSpeed)
            self.player = player_front
            self.dir = vec(0, 1)
            self.image = pygame.image.load(path.join(self.imgFolder, player_front)).convert_alpha()

        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if self.lastshoot + shootfq < now:
                self.lastshoot = now
                direction = self.dir
                (x, y) = self.rect.midleft
                Bullet(self.game, x, y, direction)
                self.game.shootsnd.play()

        if self.playerHealth <= 0:
            self.ending = ending[0]
            self.game.playing = False


    def get_mousePressed(self):
        pass

    def update(self):

        self.get_keyPressed()
        self.pos += self.vel * self.game.dt  #update pos with key pressed
        self.rect.centerx = self.pos.x
        collide_with_obs(self, self.game.obs, "x") # check collide
        self.rect.centery = self.pos.y
        collide_with_obs(self, self.game.obs, "y")

        if self.playerSan / playerStat["SAN"] < 0.5:
           self.crazy = True
           now = pygame.time.get_ticks()
           if self.lastcrazy + crazyfq < now:
               self.lastcrazy = now
               self.playerHealth -= crazydmg

        if self.playerSan / playerStat["SAN"] >= 0.5:
            self.crazy = False

    def add_HP(self, amt):
        self.playerHealth += amt
        if self.playerHealth > playerStat["CON"]:
            self.playerHealth = playerStat["CON"]

    def add_SAN(self, amt):
        self.playerSan += amt
        if self.playerSan > playerStat["SAN"]:
            self.playerSan = playerStat["SAN"]
        if self.playerSan > 0.5 * playerStat["SAN"]:
            self.crazy == False

class Shaggai(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.shaggai
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.shaggai_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.rot = 0
        self.sgaiHealth = sgaiHealth
        self.sgaiSpeed = random.choice(shaggaiSpeed)
        self.lastshoot = 0
        self.sgdmg = random.choice(sgaiDamage)


    def avoid(self):
        for sg in self.game.shaggai:
            if sg != self:
                dist = self.pos - sg.pos
                if dist != 0:
                    unitvec = dist.normalize()
                    if 0 < dist.length() < avoidR:
                        self.dv += unitvec


    def update(self):

        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.rect.center = self.pos
        self.dv = vec(1, 0).rotate(-self.rot)
        self.avoid()
        self.dv.scale_to_length(self.sgaiSpeed )
        self.dv -= 0.8*self.vel
        self.vel += self.dv * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5*self.dv*self.game.dt**2
        self.rect.centerx = self.pos.x
        collide_with_obs(self, self.game.obs, "x")
        self.rect.centery = self.pos.y
        collide_with_obs(self, self.game.obs, "y")
        if self.sgaiHealth <= 0:
            self.kill()

        now = pygame.time.get_ticks()
        if self.lastshoot + magicfq < now:
            self.lastshoot = now
            dist = self.game.player.pos - self.pos
            direction = dist.normalize()
            (x, y) = self.rect.center
            Sgmagic(self.game, x, y, direction)


class Amy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.Amy_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.talk = {
                     "talk_1" : "If you want to leave, take this key and drive away."
                     }
        self.friendly = True

    def update(self):
        pass



class Dismal(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.Dismal_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.talk = {
                     "talk_1" :"If want to see more, take this book and go to the forest under old church"
                     }
        self.friendly = True

    def update(self):
        pass



class Boss(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.BOSS_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.friendly = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.all_sprites, game.bullet
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.vel = direction * bulletV
        self.drawtime = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.drawtime > bulletLast:
            self.kill()
        if pygame.sprite.spritecollide(self, self.game.obs, False):
            self.kill()


class Sgmagic(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.all_sprites, game.sgmagic
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.sgmagic_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.vel = direction * magicV
        self.drawtime = pygame.time.get_ticks()
        self.mgdmg = random.choice(sgaiMagic)

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.drawtime > magicLast:
            self.kill()


class Aid(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.aid
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.aid_imgs[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = (x, y)



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.obs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
