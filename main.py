###
# code cite:

# pygame framework, enermy chasing and tiled map import is from:
# Chris Bradfield Tutorial of pygame gamedevelopment
# https://www.youtube.com/watch?v=VO8rTszcW4s&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=1

# NPC talking and interation learn from:
# justinmeister The-Stolen-Crown-RPG
# https://github.com/justinmeister/The-Stolen-Crown-RPG

'''
Arts by:
OpenGameArt Nicu B. 2004-2019 nicubunu.ro licenses: CC Creative Commons
https://opengameart.org/content/magic-stones

OpenGameArt rubberduck licenses: CC0 PUBLIC DOMAIN
https://opengameart.org/content/customizable-character-pack

BizmasterStudios license: CC-BY 4.0
https://opengameart.org/content/key-icons

AnthonyMyers license: CC-BY 3.0
https://opengameart.org/content/spell-book

AndHeGames CC0
https://indienova.com/resource/r/swtbcreatures-icon

Thomas Hansen CCBY
https://indienova.com/resource/r/rpg-maker-xp-tkhbslrpgm-xp-tiles-seaside-forest

Hyptosis CCBY
https://opengameart.org/content/lots-of-free-2d-tiles-and-sprites-by-hyptosis


Sound by:
FoxSynergy license: CC-BY 3.0
https://opengameart.org/content/rpg-simple-shop-16-bit

Hitctrl license: CC-BY 3.0
https://opengameart.org/content/rpg-the-maw-of-the-witches-den
https://opengameart.org/content/rpg-music-the-lost-town
https://opengameart.org/content/the-story-so-far-rpg-title-screen-music

cynicmusic license: CC0
https://opengameart.org/content/town-theme-rpg
https://opengameart.org/content/rpg-final-fantasy-style-living-everyday

Kenny license: CC0
https://opengameart.org/content/50-rpg-sound-effects

https://www.bfxr.net/

"The Forest Awakes" by Tanner Helland
licensed under a Creative Commons Attribution-ShareAlike 3.0 License.


Font by:
Copyright (c) 2011 by vernon adams (vern@newtypography.co.uk),
with Reserved Font Names "Amatic" "Amatic Bold" and "Amatic Regular"
This Font Software is
licensed under the SIL Open Font License, Version 1.1.
'''

# install pygame and pytmx to run this game

###

import pygame
from pygame.locals import *
from settings import *
from sprites import *
from tiledmap import*
from godness import*
#from battlegui import*
import sys, os
from os import path
vec = pygame.math.Vector2



class Game(object):
    def __init__(self):
        # initialize game window
        pygame.init()
        self.screen = pygame.display.set_mode(([screenW, screenH]),HWSURFACE | DOUBLEBUF, 32)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.mixer.init()

        # load img
        gameFolder = path.dirname(__file__)
        imgFolder = path.join(gameFolder, "LibRPG")
        sngFolder = path.join(gameFolder, "snd")

        self.player_battle_img = pygame.image.load(path.join(imgFolder, player_right)).convert_alpha()
        self.action_font = path.join(imgFolder, "Amatic-Bold.TTF")

        self.map = Tiledmap(path.join(gameFolder, Map_image ))
        self.map_img = self.map.makeMap()
        self.map_rect = self.map_img.get_rect()

        self.shaggai_img = pygame.image.load(path.join(imgFolder, shaggai_img)).convert_alpha()
        self.Amy_img = pygame.image.load(path.join(imgFolder, Amy_img)).convert_alpha()
        self.Dismal_img = pygame.image.load(path.join(imgFolder, Dismal_img)).convert_alpha()
        self.bullet_img = pygame.image.load(path.join(imgFolder, bullet_img)).convert_alpha()
        self.sgmagic_img = pygame.image.load(path.join(imgFolder, sgmagic_img)).convert_alpha()
        self.key_img = pygame.image.load(path.join(imgFolder, key_img)).convert_alpha()
        self.book_img = pygame.image.load(path.join(imgFolder, book_img)).convert_alpha()
        self.HP_img = pygame.image.load(path.join(imgFolder, aid_img["HP_img"])).convert_alpha()
        self.SAN_img = pygame.image.load(path.join(imgFolder, aid_img["SAN_img"])).convert_alpha()
        self.aid_imgs = {"HP" : self.HP_img, "SAN" : self.SAN_img}
        self.BOSS_img = pygame.image.load(path.join(imgFolder, boss_img)).convert_alpha()

        self.themesnd = pygame.mixer.music.load(path.join(sngFolder, theme_snd))
        self.shootsnd = pygame.mixer.Sound(path.join(sngFolder, shoot_snd))



    def new(self):
        # start a new game
        self.all_sprites = pygame.sprite.Group()
        self.obs = pygame.sprite.Group()
        self.shaggai = pygame.sprite.Group()
        self.bullet = pygame.sprite.Group()
        self.sgmagic = pygame.sprite.Group()
        self.aid = pygame.sprite.Group()

        for tile_object in self.map.loadmap.objects:
            if tile_object.name == "Player":
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "Shaggai":
                Shaggai(self, tile_object.x, tile_object.y)

            if tile_object.name == "Obs":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

            if tile_object.name == 'Amy':
                self.Amy = Amy(self, tile_object.x, tile_object.y)

            if tile_object.name == 'Car':
                self.carRect = pygame.Rect(tile_object.x, tile_object.y, tile_object.width, tile_object.height)

            if tile_object.name == 'Dismal':
                self.Dismal = Dismal(self, tile_object.x, tile_object.y)

            if tile_object.name in ['HP', 'SAN']:
                Aid(self, tile_object.x, tile_object.y, tile_object.name)

            if tile_object.name == 'Azathoth':
                self.boss = Boss(self, tile_object.x, tile_object.y)

        self.window = Scrollwindow(self.map.width, self.map.height)
        self.debug = False
        self.playerManu = False
        self.draw_dialoge = False
        self.talkingNPC = None
        self.ending = None
        self.inventory = dict()
        self.inventory["key"] = False
        self.inventory["book"] = False


        self.run()


    def run(self):
        # game loop
        self.playing = True
        pygame.mixer.music.play(loops = -1)
        pygame.mixer.music.set_volume(0.1)
        while self.playing:
            self.mouse = pygame.mouse.get_pos()
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        self.window.update(self.player)
        # sg hits player
        sg_player = pygame.sprite.spritecollide(self.player, self.shaggai, False)
        for sg in sg_player:
            self.player.playerHealth -= sg.sgdmg
            sg.vel = vec(0, 0)
            if self.player.playerHealth <= 0:
                self.ending = ending[0]
                self.playing = False
        if sg_player:
            if sg_player[0].rect.centerx > self.player.rect.midright[0]:
                self.player.pos[0] += knockback
            if sg_player[0].rect.centerx < self.player.rect.midleft[0]:
                self.player.pos[0] -= knockback
            if sg_player[0].rect.centery > self.player.rect.midbottom[1]:
                self.player.pos[1] -= knockback
            if sg_player[0].rect.centery < self.player.rect.midtop[1]:
                self.player.pos[1] += knockback

        # bullet hits Shaggai
        bullet_sg = pygame.sprite.groupcollide(self.shaggai, self.bullet, False, True)
        for sg in bullet_sg:
            sg.sgaiHealth -= bulletdmg
            sg.vel = vec(-1, -1)

        # sgmagic hits player
        sgmagic_player = pygame.sprite.spritecollide(self.player, self.sgmagic, False)
        for mag in sgmagic_player:
            self.player.playerSan -= mag.mgdmg
            if self.player.playerSan < 0:
                self.player.playerSan = 0

            if self.player.playerHealth <= 0:
                self.ending = ending[0]
                self.playing = False
            mag.kill()


        # player hits the car with key
        if self.player.rect.colliderect(self.carRect):
            if self.inventory["key"] == True:
                self.ending = ending[1]
                self.playing = False


        # player hits the boss with book
        if self.player.rect.colliderect(self.boss.rect):
            if self.inventory["book"] == True:
                self.ending = ending[2]
                self.playing = False


        # pickup aid
        aid_player = pygame.sprite.spritecollide(self.player, self.aid, False)
        for hit in aid_player:
            if hit.type == "HP":
                if self.player.playerHealth < playerStat["CON"]:
                    hit.kill()
                    self.player.add_HP(aidHP)

            if hit.type == "SAN":
                if self.player.playerSan < playerStat["SAN"]:
                    hit.kill()
                    self.player.add_SAN(aidSAN)

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_h:
                    self.debug = not self.debug
                if event.key == pygame.K_i:
                    self.playerManu = not self.playerManu
                if event.key == pygame.K_RETURN:
                    self.new()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                rectLoc = self.window.apply_rect(self.Amy.rect)
                if rectLoc.collidepoint(pos):
                    self.draw_dialoge = not self.draw_dialoge
                    self.talkingNPC = "Amy"
                    self.inventory["key"] = True

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                rectLoc = self.window.apply_rect(self.Dismal.rect)
                if rectLoc.collidepoint(pos):
                    self.draw_dialoge = not self.draw_dialoge
                    self.talkingNPC = "Dismal"
                    self.inventory["book"] = True


    def draw_text(self, text, font_name, size, color, x, y, align = "nw"):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "midtop":
            text_rect.midtop = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):

        self.screen.blit(self.map_img, self.window.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.window.apply(sprite)
            )
            if self.debug == True:
                pygame.draw.rect(self.screen, yellow, self.window.apply_rect(sprite.rect),1)

        if self.debug == True:
            for obs in self.obs:
                pygame.draw.rect(self.screen, yellow, self.window.apply_rect(obs.rect),1)

        if self.playerManu == True:
            Manurect = pygame.Rect(4*screenW // 5, 0, screenW // 5, screenH)
            self.screen.fill(white, Manurect)
            # health
            text_CON = "CON : %d / %d" % (self.player.playerHealth, playerStat["CON"])
            textY = Manurect.midtop[1] + 1*screenW // 20
            self.draw_text(text_CON, self.action_font, 30, red, Manurect.midtop[0], textY, align = "midtop")

            # san
            text_SAN = "SAN : %d / %d" % (self.player.playerSan, playerStat["SAN"])
            textY = Manurect.midtop[1] + 2*screenW // 20
            self.draw_text(text_SAN, self.action_font, 30, red, Manurect.midtop[0], textY, align = "midtop")

            # crazy
            text_CRAZY = "CRAZY : %s" % (str(self.player.crazy))
            textY = Manurect.midtop[1] + 3*screenW // 20
            self.draw_text(text_CRAZY, self.action_font, 30, red, Manurect.midtop[0], textY, align = "midtop")

            # draw inventory
            if self.inventory["key"] == True:
                keyRect = pygame.Rect(0 ,0, 32, 32)
                keyRect.centery = Manurect.midtop[1] + 10*screenW // 20
                keyRect.centerx = Manurect.midtop[0]
                self.screen.blit(self.key_img, keyRect)

            if self.inventory["book"] == True:
                bookRect = pygame.Rect(0 ,0, 32, 32)
                bookRect.centery = Manurect.midtop[1] + 11*screenW // 20
                bookRect.centerx = Manurect.midtop[0]
                self.screen.blit(self.book_img, bookRect)

        if self.draw_dialoge == True:

            self.screen.fill(black, talkwindow)
            if self.talkingNPC == "Amy":
                text = self.Amy.talk["talk_1"]
                textX = talkwindow.centerx
                textY = talkwindow.centery
                self.draw_text(text, self.action_font, 38, white, textX, textY, align = "center")


            if self.talkingNPC == "Dismal":
                text = self.Dismal.talk["talk_1"]
                textX = talkwindow.centerx
                textY = talkwindow.centery
                self.draw_text(text, self.action_font, 38, white, textX, textY, align = "center")



        pygame.display.update()
        pygame.display.flip()



    def start_screen(self):
        self.screen.fill(black)
        sgRect = self.shaggai_img.get_rect()
        sgRect.centerx = screenW // 2
        sgRect.centery = screenH // 2
        self.screen.blit(self.shaggai_img, sgRect)
        text = "Press any key to start"
        self.draw_text(text, self.action_font, 38, white, screenW // 2,  3 * screenH // 4, align = "center")
        pygame.display.flip()
        self.startwait()

    def startwait(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    waiting = False


    def wait(self):
        waiting  = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False

    def over_screen(self):
        self.screen.fill(black)
        if self.ending == ending[0]:
            text = ending[0]
            self.draw_text(text, self.action_font, 38, red, screenW // 2, screenH // 2, align = "center")
            self.draw_text("Press ENTER to start", self.action_font, 30, white, screenW // 2, 3 * screenH // 4, align = "center")
        elif self.ending == ending[1]:
            text = ending[1]
            self.draw_text(text, self.action_font, 38, yellow, screenW // 2, screenH // 2, align = "center")
            self.draw_text("Press ENTER to start", self.action_font, 30, white, screenW // 2, 3 * screenH // 4, align = "center")
        elif self.ending == ending[2]:
            text = ending[2]
            self.draw_text(text, self.action_font, 38, white, screenW // 2, screenH // 2, align = "center")
            self.draw_text("Press ENTER to start", self.action_font, 30, white, screenW // 2, 3 * screenH // 4, align = "center")
        else:
            text = "GAME OVER"
            self.draw_text(text, self.action_font, 38, white, screenW // 2, screenH // 2, align = "center")

        pygame.display.flip()
        self.wait()

g = Game()
g.start_screen()
while g.running:
    # start a new game
    g.new()
    # show game over screen
    g.over_screen()

print("Thanks for playing!")
pygame.quit()
