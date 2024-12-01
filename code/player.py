import pygame
from pygame import Vector2

from settings import *
from math import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos, groups, collision_sprites, sand_sprites):
        super().__init__(groups)
        self.groups = groups
        self.load_images()
        self.state, self.frame_index = 'down', 0
        self.image  = smallerimage(pygame.image.load(join('images','player','down','0.png')).convert_alpha())
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-80,-110)
        self.hitbox_rect.move(0,40)
        self.clock = 0
        self.timedelay = False
        self.gamestop = False
        self.blocked=False

        #movement
        self.direction = pygame.Vector2(0,0)
        self.speed = 500
        self.collision_sprites = collision_sprites

        #tools
        self.tools=['Shovel','Gun']
        self.tool_index= 0
        self.selected_tool = self.tools[self.tool_index]
        #interaction
        self.sand_sprites=sand_sprites
        self.key_down_time=0 #땅파기 시작
        self.key_up_time=0 #땅파기 끝

    def load_images(self):
        self.frames = {'left': [], 'right':[] , 'up':[],'down':[]}
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('images','player',state)):
                if file_names:
                    for file_name in sorted(file_names, key = lambda x: int(x.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = smallerimage(pygame.image.load(full_path).convert_alpha())
                        self.frames[state].append(surf)


    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d])-int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s])-int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self,dt):
        if not self.timedelay:
            self.hitbox_rect.x += self.direction.x *self.speed * dt
            self.collision('horizontal')
            self.hitbox_rect.y += self.direction.y * self.speed * dt
            self.collision('vertical')
            self.rect.center = self.hitbox_rect.center

    def collision(self,direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    elif self.direction.x<0: self.hitbox_rect.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    elif self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom

    #모래 파기
    def use_shovel(self,t):
        keys = pygame.key.get_pressed()
        if self.selected_tool == 'Shovel':
            for sand in self.sand_sprites.sprites():
                if sand.rect.collidepoint(self.target_pos):
                    if t>=1000:
                        print('hello')
                        sand.damage()




    def get_target_pos(self):
        self.target_pos= self.rect.center


    def running(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            self.speed =400
        else: self.speed = 200

    def teleporting(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_LSHIFT]:
            for i in range(10):
                PlayerClone(self.rect.center+self.direction*40*i, self.image, self.groups, i*50, 150)
            # self.rect.centerx += (int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]))*10
            # self.rect.centery += (int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))*10
            self.timedelay = True
            self.hitbox_rect.center += self.direction * 280
            self.rect.center = self.hitbox_rect.center

    def specialattack(self):
        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            for i in range(41):
                radius = 200
                angle = 2*i*pi/20
                deltadirection = pygame.Vector2(radius * cos(angle),radius * sin(angle))
                PlayerClonespecial(self.rect.center + deltadirection , self.image, self.groups, 50*i, 1000, radius , angle)
                PlayerClonespecial(self.rect.center - deltadirection , self.image, self.groups, 50*i, 1000, radius , pi + angle)

    def specialattack2(self):
        if pygame.key.get_just_pressed()[pygame.K_p]:
            for i in range(21):
                radius = 200
                angle = 2*i*pi/20
                deltadirection = pygame.Vector2(0,0)
                PlayerClonespecial2(self.rect.center + deltadirection , self.image, self.groups, 50*i, 4000, radius , angle)

    def block(self):
        self.blocked = True
        self.direction = Vector2(0, 0)

    def unblock(self):
        self.blocked = False



    def animate(self,dt):
        #get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x>0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y>0 else 'up'

        #animate
        self.frame_index = self.frame_index + self.speed//(400//len(self.frames[self.state]))*dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index)%len(self.frames[self.state])]


    def update(self,dt):
        if not self.blocked:
            self.running()
            self.input()
            self.get_target_pos()
            self.animate(dt)
            self.move(dt)
            self.teleporting()
            self.specialattack()
            self.specialattack2()
#
class PlayerClone(pygame.sprite.Sprite):
    def __init__(self, pos ,surf, groups,start, life):
        super().__init__(groups)
        self.image = pygame.transform.grayscale(surf)
        self.image.set_alpha(0)
        self.rect = self.image.get_frect(center = pos)
        self.clock = pygame.time.get_ticks()
        self.life = life
        self.start = start

    def setalpha(self):
        if (pygame.time.get_ticks()-self.clock) > self.start:
            self.image.set_alpha(100)

    def update(self,dt):
        if (pygame.time.get_ticks()-self.clock) > self.start+ self.life:
            self.kill()
        self.setalpha()


class PlayerClonespecial(pygame.sprite.Sprite):
    def __init__(self, pos ,surf, groups,start, life, radius, angle):
        super().__init__(groups)
        self.image = pygame.transform.grayscale(surf)
        self.image.set_alpha(0)
        self.rect = self.image.get_frect(center = pos)
        self.clock = pygame.time.get_ticks()
        self.life = life
        self.start = start
        self.direction = Vector2(-cos(angle), -sin(angle))
        self.radius = radius
        self.position = Vector2(self.rect.center)

    def setalpha(self):
        if (pygame.time.get_ticks()-self.clock) > self.start:
            self.image.set_alpha(100)

    def move(self):
        self.rect.center += self.direction * self.radius /1000 * 100


    def update(self,dt):
        # self.life = dt * self.radius * 1000
        self.move()
        # if (pygame.time.get_ticks()-self.clock) > self.start+ self.life:
        #     self.kill()
        if self.position.distance_to(self.rect.center) >= self.radius:
            self.kill()
        self.setalpha()

class PlayerClonespecial2(pygame.sprite.Sprite):
    def __init__(self, pos ,surf, groups,start, life, radius, angle):
        super().__init__(groups)
        self.image = pygame.transform.grayscale(surf)
        self.image.set_alpha(0)
        self.rect = self.image.get_frect(center = pos)
        self.clock = pygame.time.get_ticks()
        self.life = life
        self.start = start
        self.direction = Vector2(-cos(angle), -sin(angle))
        self.radius = radius
        self.position = Vector2(self.rect.center)

    def setalpha(self):
        if (pygame.time.get_ticks()-self.clock) > self.start:
            self.image.set_alpha(100)

    def move(self):
        if (pygame.time.get_ticks()-self.clock) > 2000 - self.start:
            self.rect.center += self.direction * self.radius /1000 * 100


    def update(self,dt):
        # self.life = dt * self.radius * 1000

        if (pygame.time.get_ticks()-self.clock) > self.start+ self.life:
            self.kill()
        if self.position.distance_to(self.rect.center) <= self.radius:
            self.move()
        self.setalpha()



class Camera(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.pos = player.rect.center
        self.player = player
    def update(self,dt):
        if not self.player.timedelay:
            self.pos = self.player.rect.center