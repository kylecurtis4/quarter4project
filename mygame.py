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
    K_SPACE,
    K_1,
    K_2,
    K_3, 
    QUIT,
)
player_skin = "myjet.png"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

total_time = 0
speed = 15
spawn_rate = 500
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(player_skin).convert()
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
        if level < 3:
            self.surf = pygame.image.load("mymissile.png").convert()
        elif level >= 3:
            self.surf = pygame.image.load("mymissile2.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                  random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0,SCREEN_HEIGHT)  
                )
            )
        self.speed = speed
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        if player_score == 1500:
            self.kill()
class BombEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super(BombEnemy, self).__init__()
        self.surf = pygame.image.load("mybomb.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                
                random.randint(0,SCREEN_WIDTH), 0
                
                )
            )
        self.speed = 10
    def update(self):
            self.rect.move_ip(0, self.speed)
            #if self.rect.down < 0:
                #self.kill()
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        if level == 1:
            self.surf = pygame.image.load("mystar.png").convert()
        if level == 2: 
            self.surf = pygame.image.load("mystar1.png").convert()
        if level == 3:
            self.surf = pygame.image.load("mystar2.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
        if player_score > 1500 and player_score < 1502:
            self.kill()
        if player_score > 3000 and player_score < 3002:
            self.kill()
player_score = 0           

high_score = 0  

level = 1

pygame.init()       

myfont = pygame.font.SysFont("monospace", 15)
gameoverfont = pygame.font.SysFont("Arial", 35, bold = True, )

white = (255,255,255)
red = (255,0,0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Spawns Enemies
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, (spawn_rate))
ADDBOMBENEMY = pygame.USEREVENT + 3
pygame.time.set_timer(ADDBOMBENEMY, (3000 - total_time))
ADDCLOUD = pygame.USEREVENT + 4
pygame.time.set_timer(ADDCLOUD, 1000)


player = Player()
enemy = Enemy()
cloud = Cloud()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


clock = pygame.time.Clock()
# Sets a timer for updating score and total time
timer_interval = 10
timer_event = pygame.USEREVENT + 2
pygame.time.set_timer(timer_event, timer_interval)    

running = True
alive = False
started = False

screen.fill((16,36,119))
pygame.display.flip() 

while not started:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_1:
                player_skin = "myjet.png"
                alive = True
                started = True
            elif event.key == K_2:
                player.skin = "myjet1.png"
                alive = True
                start = True
        
while started and running:  
    
    # Process events 
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                started = False
            elif event.key == K_SPACE and not alive:
                # RESTART the game
                player = Player()
                enemy = Enemy()
                enemies = pygame.sprite.Group()
                all_sprites = pygame.sprite.Group()
                all_sprites.add(player)
                alive = True
                player_score = 0 
                total_time = 15 
            

        elif event.type == QUIT:
            running = False
            started = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        elif event.type == timer_event:
             player_score += 1
             total_time +=0.01
             if speed <= 30:
                 speed += 0.1
             if spawn_rate > 0:
                 spawn_rate - (total_time *2)
             if player_score > 1500:
                 level = 2
             if player_score > 3000:
                 level = 3
            
        elif event.type == ADDBOMBENEMY:
            if level >= 2:
                new_bombenemy = BombEnemy()
                enemies.add(new_bombenemy)
                all_sprites.add(new_bombenemy)
        
            
            
         
    if alive: 
        # Updates Player and Enemies
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys) 
        enemies.update()
        clouds.update()
        # Draws the score 
        
        #print(level) 
        if level == 1:
            screen.fill((16, 36, 119))
        elif level == 2:
            screen.fill((16,180,36))
            if player_score > 1500 and player_score < 1700:
                lvl2txt = "Level 2"
                lvl2txtlabel = myfont.render(lvl2txt, 1 , white)
                screen.blit(lvl2txtlabel, ((SCREEN_WIDTH/2) - 50, (SCREEN_HEIGHT/2) - 50))
        elif level == 3:
            screen.fill((255,180,36))
            if player_score > 3000 and player_score < 3200:
                lvl3txt = "Level 3"
                lvl3txtlabel = myfont.render(lvl3txt, 1 , white)
                screen.blit(lvl3txtlabel, ((SCREEN_WIDTH/2) - 50, (SCREEN_HEIGHT/2) - 50))
        text = "Score:" + str(player_score)
        label = myfont.render(text, 1, white)    
        screen.blit(label, (675, 15)) 
            
        
    
        # Draws the enemies 
        for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)
        # Collisions 
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            level = 1
            if player_score > high_score:
                high_score = player_score
            game_over = "Game Over"
            game_over_label = gameoverfont.render(game_over, 1 , red)
            restart = "Space to Restart"
            restart_label = myfont.render(restart, 1 , white)
            score = "Your score: " + str(player_score)
            score_label = myfont.render(score, 1 , white)
            high_score_text = "High Score: " + str(high_score)
            high_score_label = myfont.render(high_score_text, 1 , white)
            screen.fill((0,0,0))
            screen.blit(game_over_label,((SCREEN_WIDTH/2) -  75,(SCREEN_HEIGHT/2) - 50))
            screen.blit(restart_label, (345, 300))
            screen.blit(score_label, (350,325))
            screen.blit(high_score_label, (350,345))
            player_score = 0
            alive = False 
            
    
        
    

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
    