import pygame
from pygame import Vector2

from settings import *
from math import *
from game_data import *
from support import *
#모든 엔티티에 대한 내용
class Entity(pygame.sprite.Sprite):
    def __init__(self,pos,frames,groups,facing_direction):
        super().__init__(groups)

        #graphics
        self.frame_index,self.frames =0, frames
        self.facing_direction =facing_direction
        #sprite setup
        self.direction=pygame.Vector2()
        self.speed=250
        self.blocked=False
        self.pos=pos
        self.image = self.frames[self.get_state()][self.frame_index]
        self.rect=self.image.get_frect(center=pos)
    def animate(self,dt):
        self.frame_index+=ANIMATION_SPEED *dt
        self.image = self.frames[self.get_state()][int(self.frame_index%len(self.frames[self.get_state()]))]
        self.image = rescaleimage(self.image, 500, 120)
        self.rect=self.image.get_frect(center=self.pos)
    def update(self,dt):
        self.animate(dt)
    def get_state(self):
        moving=bool(self.direction)
        if moving:
            if self.direction.x!=0:
                self.facing_direction='right' if self.direction.x>0 else 'left'
            if self.direction.y!=0:
                self.facing_direction='down' if self.direction.x>0 else 'up'
        return f"{self.facing_direction}{''if moving else '_idle'}"

    def change_facing_direction(self,target_pos):
        relation = pygame.Vector2(target_pos) - pygame.Vector2(self.rect.center)
        if abs(relation.y)<30:
            self.facing_direction = 'right' if relation.x>0 else 'left'
        else:
            self.facing_direction = 'down' if relation.y>0 else 'up'

    def block(self):
        self.blocked=True
        self.direction=pygame.Vector2(0,0)
    def unblock(self):
        self.blocked=False

#스탠리가 아닌 다른 캐릭터에 관한 내용
class Character(Entity):
    z=1
    def __init__(self, pos, frames, groups, facing_direction,character_data,player):
        super().__init__(pos, frames, groups, facing_direction)
        self.character_data = character_data
        self.player=player
        # self.facing_direction=facing_direction
        # movement
        # self.view_directions = character_data['directions']


    def get_dialog(self):
        if 5>self.player.playerstat.level>=2:
            Character.z=5
        if 10>=self.player.playerstat.level>=5 and not self.player.playerstat.lizard:
            Character.z=2
        if self.player.playerstat.key:
            Character.z=4
        if self.player.playerstat.level==10:
            Character.z=3

        return self.character_data[Character.z]

    def update(self,dt):
        self.animate(dt)
#스탠리 움직이는 코드 및 스탠리 관련 코드
class Player(pygame.sprite.Sprite):
    def __init__(self,pos, groups, collision_sprites, sand_sprites,attack_sprites,attackstanley_sprites, tool_dic,playerstat):
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
        self.ifred = False
        self.specialattackcheck = True
        self.specialattackchecktime = pygame.time.get_ticks()


        #movement
        self.direction = pygame.Vector2(0,0)
        self.speed = 500
        self.collision_sprites = collision_sprites
        self.attack_sprites = attack_sprites
        self.attackstanley_sprites = attackstanley_sprites
        self.clock = pygame.time.get_ticks()
        self.clockforbullet = pygame.time.get_ticks()

        #tools
        self.selected_tool = None
        self.tools=['Shovel','Gun']
        self.tool = tool_dic
        self.tool_index = None
        print(self.tool[0].level)

        self.level = playerstat.level
        self.max_hp = STAT_DATA[self.level]['max_hp']  #
        self.need_xp = STAT_DATA[self.level]['need_xp']  #
        self.max_thirst = STAT_DATA[self.level]['max_thirst']
        self.damage = STAT_DATA[self.level]['damage']
        self.digspeed = STAT_DATA[self.level]['digspeed']
        self.stat = {'damage': self.damage, 'digspeed': self.digspeed}
        # self.selected_tool = self.tools[self.tool_index]
        self.playerstat=playerstat
        self.fonts = {
            'dialog': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 30),
            'regular': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 18),
            'small': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 14),
            'bold': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 40),
            'title': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 100),
            'explain': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 25),
            'Mr.sir': pygame.font.Font(join('font', 'HakgyoansimTuhoOTFR.otf'), 50)
        }

        #interaction
        self.sand_sprites=sand_sprites
        self.key_down_time=0 #땅파기 시작
        self.key_up_time=0 #땅파기 끝
        self.hp=playerstat.hp
        self.xp=playerstat.xp
        self.thirst=playerstat.thirst
        self.endgame=False
        self.digtime=1000/self.digspeed*60
        self.coin=playerstat.coin
        # self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        print(playerstat.coin)


    def specialattackcheckf(self):
        if self.specialattackchecktime > 10000 and not self.specialattackcheck:
            self.specialattackcheck = True
            self.specialattackchecktime = pygame.time.get_ticks()
    #basuc stats
    def stat_update(self):


        #player
        self.max_hp=STAT_DATA[self.level]['max_hp'] #
        self.need_xp=STAT_DATA[self.level]['need_xp']#
        self.max_thirst=STAT_DATA[self.level]['max_thirst']

        if self.selected_tool:
            self.damage=STAT_DATA[self.level]['damage']+self.selected_tool.plusdamage
            self.digspeed=STAT_DATA[self.level]['digspeed']+self.selected_tool.digspeed
        else:
            self.damage = STAT_DATA[self.level]['damage']
            self.digspeed = STAT_DATA[self.level]['digspeed']

        self.stat={'damage':self.damage, 'digspeed': self.digspeed}

        #tool
        for k,v in self.tool.items():
            v.tool_update()
        self.digtime = 1000 / self.digspeed * 60

        if self.xp>=self.need_xp:
            self.xp-=self.need_xp
            self.level+=1
        self.playerstat.level=self.level
        self.playerstat.hp=self.hp
        self.playerstat.xp=self.xp
        self.playerstat.thirst=self.thirst
        self.playerstat.coin=self.coin


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
                        if t>=self.digtime:
                            print('hello')
                            sand.damage()
                            self.coin+=1
                            self.xp+=5
                            #소리 넣기
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
        if self.selected_tool:
            if self.selected_tool.name=='Shovel' and self.selected_tool.skill==True:

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
                    if pygame.time.get_ticks() - self.clockforbullet > 500:
                        Bullet(angle, self.rect.center, (self.groups,self.attack_sprites))
                        self.clockforbullet = pygame.time.get_ticks()
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
            if self.selected_tool:
                if self.selected_tool.name == 'Gun' and self.selected_tool.skill== True and self.specialattackcheck:
                    for i in range(21):
                        radius = 200
                        angle = 2*i*pi/20
                        deltadirection = pygame.Vector2(0,0)
                        PlayerClonespecial2(self.rect.center + deltadirection , self.image, self.groups, 50*i, 4000, radius , angle, self.attackstanley_sprites)
                    for sprite in self.attackstanley_sprites:
                        if ((sprite.rect.x-self.rect.centerx)**2+(sprite.rect.centery - self.rect.centery)**2)**0.5 < 200:
                            sprite.kill()
                    self.specialattackcheck = False
    def block(self):
        self.blocked = True
        self.direction = Vector2(0, 0)
    def unblock(self):
        self.blocked = False
    def collisionlizard(self):
        for sprite in self.attackstanley_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                sprite.kill()
                self.hp-=10
                self.ifred = True
                print(self.hp)
    def animate(self,dt):
        #get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x>0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y>0 else 'up'

        #animate
        self.frame_index = self.frame_index + self.speed//(400//len(self.frames[self.state]))*dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index)%len(self.frames[self.state])]
        # if self.ifred:
        #      self.apply_red_effect()
        #      self.ifred = False
        # if pygame.time.get_ticks() - self.clock():

    # def apply_red_effect(self):
    #     # red_surface = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
    #     # red_surface.fill((255, 0, 0, 100))
    #     # self.image.blit(red_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    #     self.image.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    def checkkill(self):
        if self.hp < 0:
            # title_font = self.fonts['Mr.sir']
            # title_text1 = title_font.render("GAME OVER", True, COLORS['pure white'])
            # self.display_surface.blit(title_text1, (WINDOW_WIDTH // 2 - title_text1.get_width() // 2, 325))
            self.kill()
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
            self.checkkill()
            self.specialattackcheckf()
class Characterstat:
    def __init__(self):
        self.level=0
        self.xp=0
        self.hp=100
        self.thirst=10
        self.coin=1000
        self.key=False
        self.lizard=False

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
        th_surf = self.fonts['explain'].render(f'THURST         {self.player.thirst}/{self.player.max_thirst}', False, COLORS['white'])
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
                radius=12)

        draw_text_in_box(
            surface=self.display_surface,
            rect=pygame.FRect(0, 0, 200, 40).move_to(midright= topright_rect.midright+Vector2(-50,0)),
            bg_color=COLORS['white'],
            txt_surf=self.fonts['explain'].render(f'coin:   {self.player.coin}', False, COLORS['black']),
            radius=12)

        #tool
        for i in range(0,len(self.player.tool)):
            tool_surf = smallerimage2(self.tool_frame[self.player.tool[i].name])
            tool_rect = tool_surf.get_frect(midright=self.main_rect.midright+Vector2(-300,80*(i+1)))
            name_surf = self.fonts['explain'].render(f'{self.player.tool[i].name}\nlevel:{self.player.tool[i].level}/10', False, COLORS['white'])
            name_rect = name_surf.get_frect(midright=self.main_rect.midright+Vector2(-100,80*(i+1)))
            self.display_surface.blit(tool_surf, tool_rect)
            self.display_surface.blit(name_surf,name_rect)
    def get_player(self,player):
        self.player=player

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
    def __init__(self, pos, groups,attack_sprites, attackstanley_sprites,player, display_surface):
        super().__init__(groups)
        self.image = rescaleimage(pygame.image.load('images/warden/0.png'),512,256)
        self.rect = self.image.get_frect(center = (1280,1280))
        self.attackstanley_sprites = attackstanley_sprites
        self.attack_sprites = attack_sprites
        self.clockshoot = pygame.time.get_ticks()
        self.clockfireball = pygame.time.get_ticks()
        self.display_surface = display_surface
        self.groups = groups
        self.hp = 10000
        self.angle=0
        self.clockforfireballlizard = pygame.time.get_ticks()
        self.player = player
        self.shootfireballnumber =0
        self.clockshootcheck = True
        self.clockshootfireball = pygame.time.get_ticks()
        self.clockshootfireball2 = pygame.time.get_ticks()
        self.fonts = {
            'dialog': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 30),
            'regular': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 18),
            'small': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 14),
            'bold': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 40),
            'title': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 100),
            'explain': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 25),
            'Mr.sir': pygame.font.Font(join('font', 'HakgyoansimTuhoOTFR.otf'), 50)
        }


    def collisionbullet(self):
        for sprite in self.attack_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                self.hp-=self.player.damage
                print(self.hp)

    def shootlizard(self):
        if pygame.time.get_ticks() - self.clockshoot > 1500:
            for i in range(8):
                angle = 2 * i * pi / 8 +self.angle
                Lizardforshoot(angle, self.rect.center, (self.groups,self.attackstanley_sprites), self.attack_sprites)
            self.clockshoot = pygame.time.get_ticks()
            self.angle+=2*i*pi/32
    def fireballlizard(self):
        if pygame.time.get_ticks() - self.clockfireball > 2000:
            print('d')
            Lizardforfireball(self.rect.center+pygame.Vector2(100,0), self.player, (self.groups , self.attackstanley_sprites ), self.attack_sprites)
            Lizardforfireball(self.rect.center+pygame.Vector2(-100,0), self.player, (self.groups , self.attackstanley_sprites ), self.attack_sprites)
            self.clockfireball = pygame.time.get_ticks()
    def checkdie(self):
        if self.hp<=0:
            self.clockforwarden=pygame.time.get_ticks()
            while pygame.time.get_ticks() - self.clockforwarden < 3000:
                rect_x, rect_y, rect_width, rect_height = 250, 300, 780, 80
                pygame.draw.rect(self.display_surface, COLORS['pure white'], (rect_x, rect_y, rect_width, rect_height))
                title_font = self.fonts['bold']
                title_text1 = title_font.render("내가 패배했다...", True, COLORS['black'])
                self.display_surface.blit(title_text1, (WINDOW_WIDTH // 2 - title_text1.get_width() // 2, 325))
                pygame.display.update()
            self.kill()
            return
        if self.hp<=0:
            self.player.endgame = True
    def shootfireball(self):
        if 5000< pygame.time.get_ticks() - self.clockshootfireball < 10000:
            self.clockshoot2 = pygame.time.get_ticks()
            angplus = (pygame.time.get_ticks() - self.clockshootfireball)//500 * 2 * pi / 16
            for i in range(4):
                ang = pi*2*i/4 + angplus
                Fireball(ang,self.rect.center, (self.groups, self.attackstanley_sprites))
        if pygame.time.get_ticks() - self.clockshootfireball > 10000:
            self.clockshootfireball = pygame.time.get_ticks()


    def update(self, dt):
        self.shootlizard()
        self.collisionbullet()
        self.fireballlizard()
        self.shootfireball()

class Lizardforshoot(pygame.sprite.Sprite):
    def __init__(self, angle, pos, groups,attack_sprites):
        super().__init__(groups)
        self.image = rescaleimage(pygame.image.load('images/lizardimage/0.png'),512, 192)
        self.angle = angle
        self.direction = pygame.Vector2(cos(angle), sin(angle))
        self.image = pygame.transform.rotate(self.image, -degrees(angle))
        self.rect = self.image.get_frect(center=(pos[0] + 200 * cos(angle), pos[1] + 200 * sin(angle)))
        self.speed = 500
        self.attack_sprites = attack_sprites
        self.clock = pygame.time.get_ticks()
    def move(self,dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.clock >= 3000:
            self.kill()
    def collisionbullet(self):
        for sprite in self.attack_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                self.kill()

    def update(self,dt):
        self.move(dt)
        self.collisionbullet()

class Lizardforfireball(pygame.sprite.Sprite):
    def __init__(self,pos,player,groups,attack_sprites):
        super().__init__(groups)
        self.image = rescaleimage(pygame.image.load('images/lizardimage/0.png'), 512, 192)
        self.angle = 0
        self.direction = pygame.Vector2(cos(self.angle), sin(self.angle))
        self.image = pygame.transform.rotate(self.image, -degrees(self.angle))
        self.rect = self.image.get_frect(center=(pos[0] + 200 * cos(self.angle), pos[1] + 200 * sin(self.angle)))
        self.speed = 600
        self.clock = pygame.time.get_ticks()
        self.clockforchangeangle = pygame.time.get_ticks()
        self.player = player
        self.attack_sprites = attack_sprites

    def changingeangle(self):
        dx, dy = self.rect.centerx - self.player.rect.centerx, self.rect.centery - self.player.rect.centery
        self.angle = atan2(dy, dx)
        self.direction = pygame.Vector2(-cos(self.angle), -sin(self.angle))
        # newrotated_surface = pygame.transform.rotate(self.image, -degrees(ang))
        # newrotated_rect = newrotated_surface.get_frect(
        #     center=(self.rect.c + 150 * cos(ang), 40 + pos[1] + 150 * sin(ang)))
        # self.image = newrotated_surface
        # self.rect = newrotated_rect
    def move(self,dt):
        self.rect.center += self.direction * self.speed * dt
    def collisionbullet(self):
        for sprite in self.attack_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                self.kill()
    def update(self,dt):
        if pygame.time.get_ticks() - self.clockforchangeangle >= 100:
            self.changingeangle()
            self.clockforchangeangle = pygame.time.get_ticks()
        self.move(dt)
        self.collisionbullet()

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
    def __init__(self, pos ,surf, groups,start, life, radius, angle, attackstanley_sprites):
        super().__init__(groups)
        self.image = pygame.transform.grayscale(surf)
        self.image.set_alpha(0)
        self.rect = self.image.get_frect(center = pos)
        self.attackstanley_sprites = attackstanley_sprites
        self.clock = pygame.time.get_ticks()
        self.life = life
        self.start = start
        self.direction = Vector2(-cos(angle), -sin(angle))
        self.radius = radius
        self.position = Vector2(self.rect.center)

    def setalpha(self):
        if (pygame.time.get_ticks()-self.clock) > self.start:
            self.image.set_alpha(100)
    def collisionlizard(self):
        for sprite in self.attackstanley_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()

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
        self.collisionlizard()

class Camera(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.pos = player.rect.center
        self.player = player
    def update(self,dt):
        if not self.player.timedelay:
            self.pos = self.player.rect.center



class Giantlizard(pygame.sprite.Sprite):
    def __init__(self, pos, groups,attack_sprites, attackstanley_sprites,collision_sprites,player,display_surface):
        super().__init__(groups)
        self.image = rescaleimage(pygame.image.load('images/giantlizard/0.png'),512,256)
        self.rect = self.image.get_frect(center = (1280,1280))
        self.attackstanley_sprites = attackstanley_sprites
        self.attack_sprites = attack_sprites
        self.clockshoot = pygame.time.get_ticks()
        self.clockfireball = pygame.time.get_ticks()
        self.groups = groups
        self.collision_sprites = collision_sprites
        self.display_surface = display_surface
        self.hp = 2000
        self.angle=0
        self.clockf = pygame.time.get_ticks()
        self.player = player
        self.number = 0
        self.live=1
    def collisionbullet(self):
        for sprite in self.attack_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                self.hp-=self.player.damage
                print(self.hp)

    def shootlizard(self):
        if pygame.time.get_ticks() - self.clockshoot > 3000:
            for i in range(4):
                angle = 2 * i * pi / 8 +self.angle
                Lizardforshoot(angle, self.rect.center, (self.groups,self.attackstanley_sprites), self.attack_sprites)
            self.clockshoot = pygame.time.get_ticks()
            self.angle+=2*i*pi/16
    def followlizard(self):
        if pygame.time.get_ticks() - self.clockf > 5000 and self.number <5:
            self.number+=1
            for i in range(-2,3):
                Lizardmiddle((self.rect.centerx+i*100,self.rect.centery), self.player, (self.groups, self.attackstanley_sprites),self.attack_sprites,self.collision_sprites)

            self.clockf = pygame.time.get_ticks()

    def fireballlizard(self):
        if pygame.time.get_ticks() - self.clockfireball > 8000 and self.number >=5:
            for i in range(-2,3):
                Lizardfireball((self.rect.centerx+i*150,self.rect.centery), self.player, (self.groups, self.attackstanley_sprites),self.attack_sprites,self.collision_sprites)
            self.clockfireball = pygame.time.get_ticks()
    def checkdie(self):
        if self.hp<=0:
            self.kill()
            self.live=0
    def get_live(self):
        if self.live==0:
            self.live=1
            return True

    def update(self, dt):
        self.shootlizard()
        self.collisionbullet()
        self.checkdie()
        self.followlizard()
        self.fireballlizard()

class Lizardmiddle(pygame.sprite.Sprite):
    def __init__(self,pos,player,groups,attack_sprites,collision_sprites):
        super().__init__(groups)
        self.image = rescaleimage(pygame.image.load('images/lizardimage/0.png'), 512, 192)
        self.angle = -pi/2
        self.image = pygame.transform.rotate(self.image, -degrees(self.angle))
        self.rect = self.image.get_frect(center=pos)
        self.speed = 600
        self.clock = pygame.time.get_ticks()
        self.clockforchangeangle = pygame.time.get_ticks()
        self.player = player
        self.attack_sprites = attack_sprites
        dx, dy = self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery
        self.angle = atan2(dy, dx)
        self.direction = pygame.Vector2(cos(self.angle), sin(self.angle))
        self.collision_sprites = collision_sprites
        self.startclock = pygame.time.get_ticks()
        self.start = False


    def changingeangle(self):
        dx, dy = self.rect.centerx - self.player.rect.centerx, self.rect.centery - self.player.rect.centery
        self.angle = atan2(dy, dx)
        self.direction = pygame.Vector2(-cos(self.angle), -sin(self.angle))
        # newrotated_surface = pygame.transform.rotate(self.image, -degrees(ang))
        # newrotated_rect = newrotated_surface.get_frect(
        #     center=(self.rect.c + 150 * cos(ang), 40 + pos[1] + 150 * sin(ang)))
        # self.image = newrotated_surface
        # self.rect = newrotated_rect


    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def collisionbullet(self):
        for sprite in self.attack_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                self.kill()
    def collisionwall(self):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                self.kill()
    def startcheck(self):
        if pygame.time.get_ticks() - self.startclock >500: self.start = True

    def update(self, dt):

        if self.start:
            if pygame.time.get_ticks() - self.clockforchangeangle >= 400:
                self.changingeangle()
                self.clockforchangeangle = pygame.time.get_ticks()
            self.move(dt)
            self.collisionbullet()
            self.collisionwall()
        else: self.startcheck()
class Fireball(pygame.sprite.Sprite):
    def __init__(self, angle, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/fireball/0.png')
        self.image = rescaleimage(self.image, 10 ,1)
        self.rect = self.image.get_frect(center = pos)
        self.angle = angle
        self.move = pygame.Vector2(-cos(angle), -sin(angle))
        self.speed = 1000
        self.clock = pygame.time.get_ticks()
        # newrotated_surface = pygame.transform.rotate(self.image, -degrees(ang))
        # newrotated_rect = newrotated_surface.get_frect(
        #     center=(self.rect.c + 150 * cos(ang), 40 + pos[1] + 150 * sin(ang)))
        # self.image = newrotated_surface
        # self.rect = newrotated_rect
        self.image = pygame.transform.rotate(self.image, -degrees(self.angle))
        self.rect = self.image.get_frect(center = pos)

    def update(self,dt):
        self.rect.center += self.move * self.speed * dt
        if pygame.time.get_ticks() - self.clock >= 3000:
            self.kill()

class Lizardfireball(pygame.sprite.Sprite):
    def __init__(self,pos,player,groups,attack_sprites,collision_sprites):
        super().__init__(groups)
        self.image = rescaleimage(pygame.image.load('images/lizardimage/0.png'), 512, 256)
        self.angle = 0
        self.image = pygame.transform.rotate(self.image, -degrees(self.angle))
        self.rect = self.image.get_frect(center=pos)
        self.speed = 300
        self.clock = pygame.time.get_ticks()
        self.clockforchangeangle = pygame.time.get_ticks()
        self.player = player
        self.attack_sprites = attack_sprites
        dx, dy = self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery
        self.angle = atan2(dy, dx)
        self.direction = pygame.Vector2(cos(self.angle), sin(self.angle))
        self.collision_sprites = collision_sprites
        self.startclock = pygame.time.get_ticks()
        self.start = False
        self.clockforfireball = pygame.time.get_ticks()
        self.groups = groups


    def changingeangle(self):
        dx, dy = self.rect.centerx - self.player.rect.centerx, self.rect.centery - self.player.rect.centery
        self.angle = atan2(dy, dx)
        self.direction = pygame.Vector2(-cos(self.angle), -sin(self.angle))
        # self.image = pygame.transform.rotate(self.image, -degrees(self.angle))
        # self.rect = self.image.get_frect(center = self.rect.center)
        # newrotated_surface = pygame.transform.rotate(self.image, -degrees(ang))
        # newrotated_rect = newrotated_surface.get_frect(
        #     center=(self.rect.c + 150 * cos(ang), 40 + pos[1] + 150 * sin(ang)))
        # self.image = newrotated_surface
        # self.rect = newrotated_rect


    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def collisionbullet(self):
        for sprite in self.attack_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                self.kill()
    # def collisionwall(self):
    #     for sprite in self.collision_sprites:
    #         if sprite.rect.colliderect(self.rect):
    #             self.kill()
    def startcheck(self):
        if pygame.time.get_ticks() - self.startclock >500: self.start = True

    def shootfireball(self):
        if pygame.time.get_ticks() - self.clockforfireball > 300:
            Fireball(self.angle, self.rect.center, self.groups)
            self.clockforfireball = pygame.time.get_ticks()

    def update(self, dt):

        if self.start:
            if pygame.time.get_ticks() - self.clockforchangeangle >= 400:
                self.changingeangle()
                self.clockforchangeangle = pygame.time.get_ticks()
            self.move(dt)
            self.collisionbullet()
            # self.collisionwall()
            self.shootfireball()
        else: self.startcheck()


class Fireball(pygame.sprite.Sprite):
    def __init__(self, angle, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/fireball/0.png')
        self.image = rescaleimage(self.image, 10 ,1)
        self.rect = self.image.get_frect(center = pos)
        self.angle = angle
        self.move = pygame.Vector2(-cos(angle), -sin(angle))
        self.speed = 1000
        self.clock = pygame.time.get_ticks()
        # newrotated_surface = pygame.transform.rotate(self.image, -degrees(ang))
        # newrotated_rect = newrotated_surface.get_frect(
        #     center=(self.rect.c + 150 * cos(ang), 40 + pos[1] + 150 * sin(ang)))
        # self.image = newrotated_surface
        # self.rect = newrotated_rect
        self.image = pygame.transform.rotate(self.image, -degrees(self.angle))
        self.rect = self.image.get_frect(center = pos)

    def update(self,dt):
        self.rect.center += self.move * self.speed * dt
        if pygame.time.get_ticks() - self.clock >= 3000:
            self.kill()











