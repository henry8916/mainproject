import pygame

from settings import *
from player import *
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from tool import *
from support import *
class Game:
    def __init__(self):
        #settings


        pygame.init()
        self.display_surface  = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Holes')
        self.clock = pygame.time.Clock()
        self.running = True
        self.key_down_time=0

        # tool
        self.player_tools={
            0:Tool('Shovel',1),
            1:Tool('Gun',1),
        }


        # groups
        #모든 스프라이트들 그룹
        self.all_sprites = AllSprites()
        #충돌 스트라이프들 그룹
        self.collision_sprites = pygame.sprite.Group()
        #멥 변환 발판들 그룹
        self.transition_sprites = pygame.sprite.Group()
        # 멥 변환 발판들 그룹
        self.attack_sprites = pygame.sprite.Group()
        self.attackstanley_sprites = pygame.sprite.Group()
        #땅팔 수 있는 모래들 그룹
        self.sand_sprites=pygame.sprite.Group()
        #숍이나 트레이닝센터 그룹
        self.train_sprites=pygame.sprite.Group()



        # transition/tint
        self.transition_target = None
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_mode = 'untint'
        self.tint_progress = 0
        self.tint_direction=-1
        self.tint_speed = 600


        self.import_assets()
        self.setup(self.tmx_maps['world'],'tent','world')

        #overlay
        self.tool_index=ToolIndex(self.player_tools,self.fonts,self.tool_Frames)
        self.player_index=PlayerIndex(self.player,self.fonts,pygame.image.load(join('images','player','down','0.png')),self.tool_Frames)
        self.traing_index=TrainingIndex(self.fonts,self.player,self.player_tools,self.item_Frames,self.tool_Frames['icons'])
        self.index_open=False
        self.index_open1=False
        self.index_open2=False


    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(join('holesmap', 'mainmap.tmx')), 'tent':load_pygame(join('holesmap', 'Tent.tmx')), 'wardenhouse':load_pygame(join('holesmap', 'Wardenhouse.tmx')), 'hole':load_pygame(join('holesmap', 'holes.tmx')),'centerhouse':load_pygame(join('holesmap', 'finalbattle.tmx')), 'battlefield':load_pygame(join('holesmap','battlefield.tmx'))}
        self.tool_Frames={ 'icons': {'Shovel': pygame.image.load(join('icons','shovel-removebg-preview.png')).convert_alpha(),'Gun': pygame.image.load(join('icons','gun-removebg-preview.png')).convert_alpha()},
                           'tools': {}
        }
        self.item_Frames={'HP_potion':pygame.image.load(join('icons','shovel-removebg-preview.png')),'XP_potion':pygame.image.load(join('icons','shovel-removebg-preview.png')),'THIRST_potion':pygame.image.load(join('icons','shovel-removebg-preview.png'))}
        self.fonts={
            'dialog':pygame.font.Font(join('font','Moneygraphy-Rounded.ttf'),30),
            'regular':pygame.font.Font(join('font','Moneygraphy-Rounded.ttf'),18),
            'small':pygame.font.Font(join('font','Moneygraphy-Rounded.ttf'),14),
            'bold':pygame.font.Font(join('font','Moneygraphy-Rounded.ttf'),40),
            'explain': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 25),
        }


        #sprites
    def setup(self, tmx_map, player_start_pos,map):

        #map clear
        for group in (self.all_sprites, self.collision_sprites, self.transition_sprites):
            group.empty()

        for obj in tmx_map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x*2, obj.y*2),doublingimage(obj.image),(self.all_sprites, self.collision_sprites))
        if map=='hole':
            for obj in tmx_map.get_layer_by_name('Sand'):
                SandSprite((obj.x * 2, obj.y * 2), doublingimage(obj.image), (self.all_sprites, self.sand_sprites))

        #gound
        for x,y,image in tmx_map.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE), doublingimage(image), self.all_sprites)


        #collision sprite
        for obj in tmx_map.get_layer_by_name('Collision'):
            CollisionSprite((obj.x*2, obj.y*2),pygame.Surface((obj.width*2,obj.height*2)),self.collision_sprites)
        #transision
        for obj in tmx_map.get_layer_by_name('Transition'):
            # print(obj.properties)
            TransitionSprite((obj.x*2, obj.y*2),pygame.Surface((obj.width*2,obj.height*2)), (obj.properties['target'], obj.properties['pos']),self.transition_sprites)
        if map=='world':
            for obj in tmx_map.get_layer_by_name('Train'):
                TrainStripe((obj.x * 2, obj.y * 2), pygame.Surface((obj.width * 2, obj.height * 2)), obj.name, self.train_sprites)

        for obj in tmx_map.get_layer_by_name('Entities'):#타일드 멥 수정하기
            if obj.name =='Player' and obj.properties['pos']==player_start_pos:
                self.player = Player((obj.x*2, obj.y*2), self.all_sprites, self.collision_sprites, self.sand_sprites,self.attack_sprites ,self.attackstanley_sprites, self.player_tools)
                self.camera = Camera(self.player,self.all_sprites)
                # self.gun = Gun(self.player, self.all_sprites)
            if obj.name == 'Character' and obj.properties['character_id']=='warden':
                print(obj.properties)
                print('hello')
                print('hello')
                self.warden = Warden((obj.x,obj.y), self.all_sprites, self.attack_sprites, self.attackstanley_sprites,self.player)
            if obj.name == 'Character' and obj.properties['character_id']=='lizard':
               pass



    #엔터가 눌렸는지 확인한다 엔터가 눌렸다면 움직이지 못하게 하고 INDEX창을 연다
    def input(self):

        if pygame.key.get_just_pressed()[pygame.K_RETURN]:
            self.index_open = not self.index_open
            self.player.blocked=not self.player.blocked
        if pygame.key.get_just_pressed()[pygame.K_RSHIFT]:
            self.index_open1= not self.index_open1
            self.player.blocked=not self.player.blocked

    # 장소에 도착한지 확인하고 인덱스 창을 연다. 나갈 수 있도록 이동 키는 가능하게 설정
    def training_check(self):
        sprites=[sprite for sprite in self.train_sprites if sprite.rect.colliderect(self.player.hitbox_rect)]
        if sprites:
            self.index_open2=True
            self.traing_index.place=sprites[0].place
        else:
            self.index_open2=False




    # transition system
    def transition_check(self):
        sprites=[sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox_rect)]
        if sprites:
            self.player.block()
            self.transition_target=sprites[0].target
            self.tint_mode='tint'



    def tint_screen(self,dt):
        if  self.tint_mode=='untint':
            self.tint_progress -=self.tint_speed*dt

        if  self.tint_mode=='tint':
            self.tint_progress += self.tint_speed*dt
            if self.tint_progress>=255:
                print(self.transition_target)
                print(self.player.selected_tool)
                self.setup(self.tmx_maps[self.transition_target[0]],self.transition_target[1],self.transition_target[0])
                self.tint_mode='untint'
                self.transition_target=None
        self.tint_progress =max(0,min(self.tint_progress,255))
        self.tint_surf.set_alpha(self.tint_progress)
        self.display_surface.blit(self.tint_surf,(0,0))


    def run(self):
        while self.running:

            dt = self.clock.tick() / 1000
            self.display_surface.fill('black')

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                    self.key_down_time = pygame.time.get_ticks()  # O 키를 눌렀을 때 시간 기록
                    self.player.blocked=True
                if event.type == pygame.KEYUP and event.key == pygame.K_o:
                    self.t = pygame.time.get_ticks()-self.key_down_time# O 키를 뗐을 때 초기화
                    self.player.use_shovel(self.t)
                    self.key_down_time=0
                    self.player.blocked = False

                self.player.mousedbuttondown = True if event.type == pygame.MOUSEBUTTONDOWN else False
                self.player.mousedbuttonup = True if event.type == pygame.MOUSEBUTTONUP else False
            #updatedb
            if not self.player.gamestop:
                self.input()
                self.transition_check()
                self.training_check()
                self.all_sprites.update(dt)


            #draw
            self.all_sprites.draw(self.camera.pos,self.player)
            if self.player.timedelay:
                clock = pygame.time.get_ticks()
                while (pygame.time.get_ticks() - clock) < 200:
                    pass
                self.player.timedelay = False

            # overlays
            #if self.dialog_tree: self.dialog_tree.update()s
            if self.index_open:
                self.tool_index.update(dt)
            if self.index_open1:
                self.player_index.update(dt)
            if self.index_open2:
                self.traing_index.update()

            self.player.get_current_tool(self.tool_index.selected_tool)
            if self.key_down_time:
                draw_bar(
                surface=self.display_surface,
                rect=pygame.FRect(0,0,100,20).move_to(midbottom=Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-70)),
                value=pygame.time.get_ticks()-self.key_down_time,
                max_value=1000,
                color=COLORS['white'],
                bg_color=COLORS['black']
            )


            self.tint_screen(dt)
            pygame.display.update()







        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()

