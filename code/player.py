import pygame
from pygame import Vector2

from settings import *
from math import *
from game_data import *
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos, groups, collision_sprites, sand_sprites,attack_sprites,attackstanley_sprites, tool_dic):
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
        self.mousedbuttondown = False
        self.mousedbuttonup = False
        self.lastmouse = False
        self.gunlist = []


        #movement
        self.direction = pygame.Vector2(0,0)
        self.speed = 500
        self.collision_sprites = collision_sprites
        self.attack_sprites = attack_sprites
        self.attackstanley_sprites = attackstanley_sprites

        #tools
        self.selected_tool = None
        self.tools=['Shovel','Gun']
        self.tool = tool_dic
        self.tool_index = None

        # self.selected_tool = self.tools[self.tool_index]
        #interaction
        self.sand_sprites=sand_sprites
        self.key_down_time=0 #땅파기 시작
        self.key_up_time=0 #땅파기 끝
        self.level = 0
        self.hp=90
        self.xp=25
        self.thirst=10

    #basuc stats
    def stat_update(self):
        self.max_hp=STAT_DATA[self.level]['max_hp'] #
        self.need_xp=STAT_DATA[self.level]['need_xp']#
        self.max_thirst=STAT_DATA[self.level]['max_thirst']
        self.damage=STAT_DATA[self.level]['damage']
        self.digspeed=STAT_DATA[self.level]['digspeed']
        self.stat={'damage':self.damage, 'digspeed': self.digspeed}
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

    #삽으로 모래파기
    def use_shovel(self,t):
        if  self.selected_tool !=None:
            if self.selected_tool.name == 'Shovel':
                for sand in self.sand_sprites.sprites():
                    if sand.rect.collidepoint(self.target_pos):
                        if t>=1000:
                            print('hello')
                            sand.damage()
    #타깃 즉 모래위치
    def get_target_pos(self):
        self.target_pos= self.rect.center

    #현재 장비 입력받기
    def get_current_tool(self,tool):
        self.selected_tool=tool

    def running(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            self.speed = 1000
        else: self.speed = 500
    def teleporting(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE]:
            for i in range(10):
                PlayerClone(self.rect.center+self.direction*40*i, self.image, self.groups, i*50, 150)
            # self.rect.centerx += (int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]))*10
            # self.rect.centery += (int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))*10
            self.timedelay = True
            self.hitbox_rect.center += self.direction * 280
            self.rect.center = self.hitbox_rect.center
    #일반공격 삽,총
    def normalattack(self):

        # dx, dy = pygame.mouse.get_pos()[0] - WINDOW_WIDTH / 2, pygame.mouse.get_pos()[1] - WINDOW_HEIGHT / 2
        # angle = atan2(dy, dx)
        # gun = Gun(angle, self.rect.center, self.groups)
        # gunlist = []

        if self.selected_tool != None:
            if pygame.mouse.get_pressed()[0] and not self.lastmouse:
                dx, dy = pygame.mouse.get_pos()[0] - WINDOW_WIDTH / 2, pygame.mouse.get_pos()[1] - WINDOW_HEIGHT / 2
                angle = atan2(dy, dx)

                if self.selected_tool.name == 'Shovel':
                    shovel = Shovel(angle, self.rect.center, self.groups)
                    self.gunlist = [shovel]
                elif self.selected_tool.name == 'Gun':
                    gun = Gun(angle, self.rect.center, self.groups)
                    self.gunlist = [gun]
            elif pygame.mouse.get_pressed()[0]:
                dx, dy = pygame.mouse.get_pos()[0] - WINDOW_WIDTH / 2, pygame.mouse.get_pos()[1] - WINDOW_HEIGHT / 2
                angle = atan2(dy, dx)
                if self.gunlist:
                    self.gunlist[0].changingeangle(angle, self.rect.center)
            elif not pygame.mouse.get_pressed()[0] and self.lastmouse:
                dx, dy = pygame.mouse.get_pos()[0] - WINDOW_WIDTH / 2, pygame.mouse.get_pos()[1] - WINDOW_HEIGHT / 2
                angle = atan2(dy, dx)
                if self.selected_tool.name == 'Shovel':
                    ShovelBullet(angle, self.rect.center, self.groups)
                elif self.selected_tool.name == 'Gun':
                    Bullet(angle, self.rect.center, (self.groups,self.attack_sprites))
                if self.gunlist:
                    self.gunlist[0].kill()
            self.lastmouse = pygame.mouse.get_pressed()[0]
    #기타 등등
    def specialattack(self):
        if pygame.key.get_just_pressed()[pygame.K_l]:
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
    def collisionlizard(self):
        for sprite in self.attackstanley_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                self.hp-=10
                self.apply_red_effect()
    def animate(self,dt):
        #get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x>0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y>0 else 'up'

        #animate
        self.frame_index = self.frame_index + self.speed//(400//len(self.frames[self.state]))*dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index)%len(self.frames[self.state])]
    def apply_red_effect(self):
        red_surface = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
        red_surface.fill((255, 0, 0, 100))
        self.image.blit(red_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

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
            self.normalattack()
            self.collisionlizard()
            self.stat_update()

class PlayerIndex:
    def __init__(self,player,fonts,image,tool_frame):
        self.display_surface=pygame.display.get_surface()
        self.fonts=fonts
        self.player=player
        self.image=image

        #frames
        #이미지 처러 혹시 필요하면 함수에서 입력받아 사용하기

        #tint surf
        self.tint_surf =pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surf.set_alpha(200)

        self.main_rect = pygame.FRect(0,0,WINDOW_WIDTH*0.6, WINDOW_HEIGHT*0.8).move_to(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.tool_frame=tool_frame['icons']

    def display_main(self):
        rect=pygame.FRect(self.main_rect.left ,self.main_rect.top, self.main_rect.width, self.main_rect.height)
        surf=pygame.Surface((rect.width,rect.height))
        surf.set_alpha(200)
        pygame.draw.rect(self.display_surface, COLORS['dark'], rect, 0, 12,12, 12,0)

        #display your image and item image
        #payer 모습
        topleft_rect = pygame.FRect(rect.topleft,(rect.width*0.4,rect.height*0.4))
        pygame.draw.rect(self.display_surface, COLORS['red'],topleft_rect,0,0,12,0)

        topright_rect=pygame.FRect(self.main_rect.left + rect.width*0.4, self.main_rect.top,self.main_rect.width - rect.width*0.4, self.main_rect.height*0.15)
        pygame.draw.rect(self.display_surface, COLORS['gold'], topright_rect, 0, 0, 0, 12)

        topright2_rect = pygame.FRect(self.main_rect.left + rect.width * 0.4, self.main_rect.top+rect.height * 0.15, self.main_rect.width - rect.width * 0.4, self.main_rect.height * 0.25)
        pygame.draw.rect(self.display_surface, COLORS['gray'], topright2_rect)


        #사람 이미지
        tool_surf =smallerimage2(self.image)
        tool_rect = tool_surf.get_frect(center = topleft_rect.center)
        self.display_surface.blit(tool_surf,tool_rect)

        #name
        name_surf=self.fonts['bold'].render('Stanley',False,COLORS['white'])
        name_rect=name_surf.get_frect( topleft= topright_rect.topleft )
        self.display_surface.blit(name_surf,name_rect)

        ##level
        level_surf = self.fonts['explain'].render(f'level: {self.player.level}/10', False, COLORS['white'])
        level_rect = level_surf.get_frect(topleft=topleft_rect.topright+Vector2(10,50))
        self.display_surface.blit(level_surf, level_rect)

        #HP
        hp_surf = self.fonts['explain'].render(f'HP              {self.player.hp}/{self.player.max_hp}', False, COLORS['white'])
        hp_rect = hp_surf.get_frect(midleft=topright2_rect.midleft + Vector2(10,-20))
        self.display_surface.blit(hp_surf, hp_rect)
        draw_bar(
            surface=self.display_surface,
            rect=pygame.FRect(0,0,400,30).move_to(midleft=topright2_rect.midleft + Vector2(10,-20)),
            value=self.player.hp,
            max_value= self.player.max_hp,
            color= COLORS['fire'],
            bg_color= COLORS['black']
        )
        self.display_surface.blit(hp_surf, hp_rect)


        #THurst
        th_surf = self.fonts['explain'].render(f'THURST         {self.player.xp}/{self.player.need_xp}', False, COLORS['white'])
        th_rect = th_surf.get_frect(midleft=topright2_rect.midleft + Vector2(10, 20))
        self.display_surface.blit(th_surf, th_rect)
        draw_bar(
            surface=self.display_surface,
            rect=pygame.FRect(0,0,400,30).move_to(midleft=topright2_rect.midleft + Vector2(10, 20)),
            value=self.player.thirst,
            max_value=self.player.max_thirst,
            color=COLORS['water'],
            bg_color=COLORS['black']
        )
        self.display_surface.blit(th_surf, th_rect)

        #XP
        xp_surf = self.fonts['explain'].render(f'XP             {self.player.xp}/{self.player.need_xp}', False, COLORS['white'])
        xp_rect = xp_surf.get_frect(midtop=self.main_rect.midbottom + Vector2(0,-self.main_rect.height*0.6+20))
        self.display_surface.blit(xp_surf, xp_rect)
        draw_bar(
            surface=self.display_surface,
            rect=pygame.FRect(0, 0, 700, 30).move_to( midtop=self.main_rect.midbottom + Vector2(0, -self.main_rect.height*0.6+20)),
            value=self.player.xp,
            max_value=self.player.need_xp,
            color=COLORS['gold'],
            bg_color=COLORS['black']
        )
        self.display_surface.blit(xp_surf, xp_rect)

        #stat
        i=0
        for k,v in self.player.stat.items():
            i+=1
            draw_text_in_box(
                surface=self.display_surface,
                rect=pygame.FRect(0,0,200,40).move_to(midleft=self.main_rect.midleft+Vector2(50,80*i)),
                bg_color=COLORS['white'],
                txt_surf=self.fonts['regular'].render(f'{k}         {v}', False, COLORS['black']),
                )


        #tool
        for i in range(0,len(self.player.tool)):
            tool_surf = smallerimage2(self.tool_frame[self.player.tool[i].name])
            tool_rect = tool_surf.get_frect(midright=self.main_rect.midright+Vector2(-300,80*(i+1)))
            name_surf = self.fonts['explain'].render(f'{self.player.tool[i].name}\nlevel:{self.player.tool[i].level}/10', False, COLORS['white'])
            name_rect = name_surf.get_frect(midright=self.main_rect.midright+Vector2(-100,80*(i+1)))
            self.display_surface.blit(tool_surf, tool_rect)
            self.display_surface.blit(name_surf,name_rect)

    def update(self,dt):
        #input
        self.display_surface.blit(self.tint_surf,(0,0))
        #tint the main game
        #display the list
        self.display_main()


#tool classes
class Gun(pygame.sprite.Sprite):
    def __init__(self, angle, pos, groups):
        super().__init__(groups)
        self.rect_width = 300
        self.rect_height = 50
        self.overlay = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        self.clock = pygame.time.get_ticks()
        pygame.draw.rect(self.overlay, (255,0,0,40), (0, 0, self.rect_width, self.rect_height))
        rotated_surface = pygame.transform.rotate(self.overlay, -degrees(angle))
        rotated_rect = rotated_surface.get_frect(center=(pos[0]+150*cos(angle), 40+pos[1]+150*sin(angle)))
        self.image = rotated_surface
        self.rect = rotated_rect
        self.mousedbuttondown = False
        self.mousedbuttonup = False
        self.lastmouse = False
        self.gunlist = []
        self.groups=groups
    def changingeangle(self,ang,pos):
        newrotated_surface = pygame.transform.rotate(self.overlay, -degrees(ang))
        newrotated_rect = newrotated_surface.get_frect(center=(pos[0]+150*cos(ang),40+ pos[1]+150*sin(ang)))
        self.image = newrotated_surface
        self.rect = newrotated_rect
    def update(self, dt):
        pass
class Shovel(pygame.sprite.Sprite):
    def __init__(self, angle, pos, groups):
        super().__init__(groups)
        self.rect_width = 100
        self.rect_height = 80
        self.overlay = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        self.clock = pygame.time.get_ticks()
        pygame.draw.rect(self.overlay, (255,0,0,40), (0, 0, self.rect_width, self.rect_height))
        rotated_surface = pygame.transform.rotate(self.overlay, -degrees(angle))
        rotated_rect = rotated_surface.get_frect(center=(pos[0]+50*cos(angle), 40+pos[1]+50*sin(angle)))
        self.image = rotated_surface
        self.rect = rotated_rect
    def changingeangle(self,ang,pos):
        newrotated_surface = pygame.transform.rotate(self.overlay, -degrees(ang))
        newrotated_rect = newrotated_surface.get_frect(center=(pos[0]+50*cos(ang),40+ pos[1]+50*sin(ang)))
        self.image = newrotated_surface
        self.rect = newrotated_rect
        print('d')
    def update(self, dt):
        pass

#attack image
class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/gun/bullet.png')
        self.rect = self.image.get_frect(center = pos+Vector2(0,40))
        self.angle = angle
        self.move = pygame.Vector2(cos(angle), sin(angle))
        self.speed = 1000
        self.clock = pygame.time.get_ticks()
    def update(self,dt):
        self.rect.center += self.move * self.speed * dt
        if pygame.time.get_ticks() - self.clock >= 1000:
            self.kill()
class ShovelBullet(pygame.sprite.Sprite):
    def __init__(self, angle, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/gun/bullet.png')
        self.rect = self.image.get_frect(center=pos+Vector2(0,40))
        self.angle = angle
        self.move = pygame.Vector2(cos(angle), sin(angle))
        self.speed = 1000
        self.clock = pygame.time.get_ticks()
    def update(self,dt):
        self.rect.center += self.move * self.speed * dt
        if pygame.time.get_ticks() - self.clock >= 100:
            self.kill()


class Warden(pygame.sprite.Sprite):
    def __init__(self, pos, groups,attack_sprites, attackstanley_sprites):
        super().__init__(groups)
        self.image = rescaleimage(pygame.image.load('images/warden/0.png'),512,256)
        self.rect = self.image.get_frect(center = (1280,1280))
        self.attackstanley_sprites = attackstanley_sprites
        self.attack_sprites = attack_sprites
        self.clock = pygame.time.get_ticks()
        self.groups = groups
        self.hp = 10000
        self.angle=0

    def collisionbullet(self):
        for sprite in self.attack_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                self.hp-=2000

    def shootlizard(self):
        if pygame.time.get_ticks() - self.clock > 500:
            for i in range(10):
                angle = 2 * i * pi / 10+self.angle
                Lizardforshoot(angle, self.rect.center, (self.groups,self.attackstanley_sprites))
            self.clock = pygame.time.get_ticks()
            self.angle+=2*i*pi/40
    def checkdie(self):
        if self.hp<=0: self.kill()
    def update(self, dt):
        self.shootlizard()
        self.collisionbullet()
        self.checkdie()

class Lizardforshoot(pygame.sprite.Sprite):
    def __init__(self, angle, pos, groups):
        super().__init__(groups)
        self.image = rescaleimage(pygame.image.load('images/lizardimage/0.png'),512, 128)
        self.angle = angle
        self.direction = pygame.Vector2(cos(angle), sin(angle))
        self.image = pygame.transform.rotate(self.image, -degrees(angle))
        self.rect = self.image.get_frect(center=(pos[0] + 200 * cos(angle), pos[1] + 200 * sin(angle)))
        self.speed = 1000
        self.clock = pygame.time.get_ticks()
    def move(self,dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.clock >= 1000:
            self.kill()
    def update(self,dt):
        self.move(dt)

#other
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