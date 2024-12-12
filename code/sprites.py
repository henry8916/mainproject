import pygame.mouse
# from pygame.examples.multiplayer_joystick import player
from math import atan2, degrees
from settings import *
import random

#스프라이트끼리의 상호작용에 관한 코드
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True
class AnimatedSprite(Sprite):
    def __init__(self,pos,frames,groups):
        self.frame_index,self.frames=0,frames
        super().__init__(pos,frames[self.frame_index],groups)
    def animate(self,dt):
        self.frame_index+=ANIMATION_SPEED * dt
        self.image=self.frames[int(self.frame_index%len(self.frames))]
    def update(self,dt):
        self.animate(dt)

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self,pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class TransitionSprite(Sprite):
    def __init__(self, pos, surf, target, groups):
        super().__init__(pos, surf, groups)
        self.target = target

class TrainStripe(Sprite):
    def __init__(self,pos,surf,place, groups):
        super().__init__(pos,surf,groups)
        self.place=place


class SandSprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)

        self.hp=1
        self.exist=True

    def damage(self):
        self.hp -= 1

        if self.hp<=0:
            self.kill()