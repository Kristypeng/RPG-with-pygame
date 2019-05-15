import pygame
vec = pygame.math.Vector2
import random
from godness import*

# define some colors (R, G, B)
white = (255, 255, 255)
black = (0, 0, 0)
darkgrey = (40, 40, 40)
lightgrey = (100, 100, 100)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
LIGHTSALMON = (255, 160, 122)
SALMON = (250, 128, 114)
LIGHTCORAL = (240, 128, 128)
LIGHTBLUE = (133, 193, 233)
DARKBLUE = (40, 116, 166)

# game settings
FPS = 60
screenW = 800
screenH = 600
title = "Escape the Town!"
tilesize = 32

# img settings

player_front = "chara_stand.png"
player_back = "chara2_back.png"
player_left = "chara2_left.png"
player_right = "chara2_right.png"
player_front_F = "chara1_stand.png"
Map_image = "NewMap.tmx"
shaggai_img = "shaggai.png"
start_img = "Start.png"
Amy_img = "Amy.png"
Dismal_img = "Dismal.png"
bullet_img = "bullet.png"
sgmagic_img = "sgmagic.png"
theme_snd = "TheForestAwakes.ogg"
shoot_snd = "Hit_Hurt2.wav"
key_img = "key.png"
book_img = "redbook.png"
boss_img = "boss.png"

# player settings

playerSpeed = 150
x,y = screenW/2, screenH/2
playerStat = {"CON": 60, "SAN": 60, "CRAZY": False}
crazydmg = 2
crazyfq = 1000
ending = ["YOU DIED", "YOU ESCAPED!", "Victory! NO MORE MONSTERS."]



# shaggai settings
shaggaiSpeed = [100, 120, 90, 110, 100]
sgaiHealth = 10
sgaiDamage = [1, 2, 3, 4, 5]
sgaiMagic = [5,6,7,8]
knockback = -10
avoidR = 60


# chat box dim
talkwindow = pygame.Rect(0, 0, screenW, screenH//5)
talkwindow.midbottom = (screenW // 2, screenH)

# bulllet
bulletV = 300
bulletLast = 1200 #ms
shootfq = 150
bulletdmg = Dice(1, 5)

# sgmagic
magicV = 200
magicLast = 1500
magicfq = 3000

# med
aid_img = {"HP_img":"HP.png", "SAN_img" :"SAN.png"}
aidHP = 20
aidSAN = 20
