# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 09:02:33 2024

@author: kcurtis26
"""

# Import the pygame module
import pygame

import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
     
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

total_time = 15
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("myjet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        #self.surf = pygame.Surface((75, 25))
        #self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
    def update(self,pressed_keys):
        if pressed_keys[K_UP]:  
            self.rect.move_ip(0,-10)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,10)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10,0)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10,0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                  random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0,SCREEN_HEIGHT)  
                )
            )
        self.speed = total_time
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
player_score = 0           

    

pygame.init()       

myfont = pygame.font.SysFont("monospace", 15)

white = (255,255,255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 300)

player = Player()
enemy = Enemy()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

clock = pygame.time.Clock()

timer_interval = 1000 # 1 seconds
timer_event = pygame.USEREVENT + 2
pygame.time.set_timer(timer_event, timer_interval)    


while running:  
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == timer_event:
             player_score += 1
             total_time +=1
        
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys) 
    enemies.update()
    text = "Score:" + str(player_score)
    label = myfont.render(text, 1, white)
    
      
        
    screen.fill((0, 0, 0))
    screen.blit(label, (675, 15))
    
    for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False
    

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
    