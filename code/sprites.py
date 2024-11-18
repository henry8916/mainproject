import pygame.mouse
# from pygame.examples.multiplayer_joystick import player
from math import atan2, degrees
from settings import *

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self,pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True

# class Gun(pygame.sprite.Sprite):
#     def __init__(self,player,groups):
#         #player connection
#         self.player = player
#         self.distance = 140
#         self.player_direction = pygame.Vector2(1,0)
#
#         #sprite setup
#         super().__init__(groups)
#         self.gun_surf = pygame.image.load(join('images','gun','gun.png')).convert_alpha()
#         self.image = self.gun_surf
#         self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)
#     def rotate_gun(self):
#         angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
#         if self.player_direction.x>0:

            # self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
    # def get_direction(self):
    #     mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    #     player_pos = pygame.Vector2((WINDOW_WIDTH/2,WINDOW_WIDTH/2))
    #     self.player_direction = (mouse_pos - player_pos).normalize()
    # def update(self, dt):
    #     self.get_direction()
    #     # self.rotate_gun()
    #     self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

#
# class Enemy(pygame.sprite.Sprite):
#     def __init__(self,pos, frames, groups, player, collision_sprites):
#         super().__init__(groups)
#         self.player = player
#
#         #image
#         self.frames = self.frame_index = frames, 0
#         self.images = self.frames[self.frame_index]
#
#         #rect
#         self.rect = self.image.get_frect(center = pos)
#         self.hitbox_rect = self.rect.inflate(-20,-40)
#         self.collision_sprites = collision_sprites
#         self.direction = pygame.Vector2()
#         self.speed = 350
#
