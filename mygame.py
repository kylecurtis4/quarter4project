# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 09:02:33 2024

@author: kcurtis26
"""

# Import the pygame module
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
    def update(self,pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
            print(self.rect.x, self.rect.y)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = Player()
running = True

while running:  
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

    screen.fill((0, 0, 0))
    
    screen.blit(player.surf, (player.rect.x, player.rect.y))

    pygame.display.flip()

pygame.quit()