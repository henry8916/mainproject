import pygame
import sys
from dialog import *
from settings import *
from player import *
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from tool import *
from support import *
class Game:
    k = 0
    def __init__(self):
        #settings


        pygame.init()
        self.display_surface  = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.state="start"
        pygame.display.set_caption('Holes')
        self.clock = pygame.time.Clock()
        self.running = True
        self.key_down_time=0

        # tool
        self.player_tools={
            0:Tool('Shovel',5),
            1:Tool('Gun',5),
        }
        self.player_stat=Characterstat()


        # groups
        #모든 스프라이트들 그룹
        self.all_sprites = AllSprites()
        #충돌 스트라이프들 그룹
        self.collision_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()
        #멥 변환 발판들 그룹
        self.transition_sprites = pygame.sprite.Group()
        # 멥 변환 발판들 그룹
        self.attack_sprites = pygame.sprite.Group()
        self.attackstanley_sprites = pygame.sprite.Group()
        #땅팔 수 있는 모래들 그룹
        self.sand_sprites=pygame.sprite.Group()
        #숍이나 트레이닝센터 그룹
        self.train_sprites=pygame.sprite.Group()
        #도마뱀
        self.giant=None
        self.dialog_tree = None



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
        self.clockforgiant = pygame.time.get_ticks()


    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(join('holesmap', 'mainmap.tmx')), 'tent':load_pygame(join('holesmap', 'Tent.tmx')), 'wardenhouse':load_pygame(join('holesmap', 'Wardenhouse.tmx')), 'hole':load_pygame(join('holesmap', 'holes.tmx')),'centerhouse':load_pygame(join('holesmap', 'finalbattle.tmx')), 'battlefield':load_pygame(join('holesmap','battlefield.tmx')), 'room':load_pygame(join('holesmap','room.tmx'))}
        self.tool_Frames={ 'icons': {'Shovel': pygame.image.load(join('icons','shovel-removebg-preview.png')).convert_alpha(),'Gun': pygame.image.load(join('icons','gun-removebg-preview.png')).convert_alpha()},
                           'tools': {}
        }
        self.item_Frames={'HP_potion':pygame.image.load('images/items/healthpo.png'),'XP_potion':pygame.image.load('images/items/bluepo.png'),'THIRST_potion':pygame.image.load('images/items/waterbottle.png')}
        self.overworld_frames = {'Characters': all_character_import('./images/zero')}
        self.item_Frames={'HP_potion':pygame.image.load('images/items/healthpo.png'),'XP_potion':pygame.image.load('images/items/bluepo.png'),'THIRST_potion':pygame.image.load(join('images/items/waterbottle.png'))}
        self.fonts={
            'dialog':pygame.font.Font(join('font','Moneygraphy-Rounded.ttf'),30),
            'regular':pygame.font.Font(join('font','Moneygraphy-Rounded.ttf'),18),
            'small':pygame.font.Font(join('font','Moneygraphy-Rounded.ttf'),14),
            'bold':pygame.font.Font(join('font','Moneygraphy-Rounded.ttf'),40),
            'title':pygame.font.Font(join('font','Moneygraphy-Rounded.ttf'),100),
            'explain': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 25),
            'Mr.sir':pygame.font.Font(join('font','HakgyoansimTuhoOTFR.otf'),50)
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
                self.player = Player((obj.x*2, obj.y*2), self.all_sprites, self.collision_sprites, self.sand_sprites,self.attack_sprites ,self.attackstanley_sprites, self.player_tools, self.player_stat)
                self.camera = Camera(self.player,self.all_sprites)
                self.tool_index = ToolIndex(self.player_tools, self.fonts, self.tool_Frames)
                self.player_index = PlayerIndex(self.player, self.fonts,
                                                pygame.image.load(join('images', 'player', 'down', '0.png')),
                                                self.tool_Frames)
                self.traing_index = TrainingIndex(self.fonts, self.player, self.player_tools, self.item_Frames,
                                                  self.tool_Frames['icons'])
                # self.gun = Gun(self.player, self.all_sprites)
            if obj.name == 'Character' and obj.properties['character_id']=='zero' :
                print(obj.x,obj.y,1001010)
                Character(pos=(obj.x*2, obj.y*2),
                          frames=self.overworld_frames['Characters']['zeroall'],
                          groups=(self.all_sprites,self.collision_sprites,self.character_sprites),
                          facing_direction = obj.properties['direction'],
                          character_data=PLAYER_DATA[obj.properties['character_id']])
            if obj.name == 'Character' and obj.properties['character_id']=='warden' and self.player.level>=10:
                print(obj.properties)
                self.warden = Warden((obj.x,obj.y), self.all_sprites, self.attack_sprites, self.attackstanley_sprites,self.player,self.display_surface)
            if obj.name == 'Character' and obj.properties['character_id']=='lizard' and self.player.level>=5:
                self.giant = Giantlizard((obj.x, obj.y), self.all_sprites, self.attack_sprites, self.attackstanley_sprites, self.collision_sprites, self.player,self.display_surface)

    #엔터가 눌렸는지 확인한다 엔터가 눌렸다면 움직이지 못하게 하고 INDEX창을 연다
    # 장소에 도착한지 확인하고 인덱스 창을 연다. 나갈 수 있도록 이동 키는 가능하게 설정
    def input(self):
        sprites = [sprite for sprite in self.train_sprites if sprite.rect.colliderect(self.player.hitbox_rect)]

        if not sprites:
            if pygame.key.get_just_pressed()[pygame.K_RETURN]:
                self.index_open = not self.index_open
                self.player.blocked = not self.player.blocked
            if pygame.key.get_just_pressed()[pygame.K_RSHIFT]:
                self.index_open1 = not self.index_open1
                self.player.blocked = not self.player.blocked

        if sprites:
            self.traing_index.place = sprites[0].place
            if pygame.key.get_just_pressed()[pygame.K_RSHIFT] and self.traing_index.place == 'Shop':
                self.index_open2 = not self.index_open2
                self.player.blocked = not self.player.blocked
            if pygame.key.get_just_pressed()[pygame.K_RETURN] and self.traing_index.place == 'Training':
                self.index_open2 = not self.index_open2
                self.player.blocked = not self.player.blocked

        if not self.dialog_tree:
            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_i]:
                for character in self.character_sprites:
                    if check_connection(200, self.player, character):
                        print('dialog')
                        self.player.block()
                        character.change_facing_direction(self.player.rect.center)
                        self.create_dialog(character)


    def create_dialog(self, character):
        if not self.dialog_tree:
            self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['explain'],
                                          self.end_dialog)

        if pygame.key.get_just_pressed()[pygame.K_RETURN]:
            self.index_open = not self.index_open
            self.player.blocked = not self.player.blocked

    def end_dialog(self, character):
        self.dialog_tree = None
        self.player.unblock()
    # 장소에 도착한지 확인하고 인덱스 창을 연다. 나갈 수 있도록 이동 키는 가능하게 설정



    # transition system
    def transition_check(self):
        sprites=[sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox_rect)]
        if sprites and (not sprites[0].target[0]=='centerhouse' or self.player.level>=10) and (not sprites[0].target[0]=='battlefield' or self.player.level>=5):
        # if sprites:
            print(self.player.level)
            print(sprites[0].target[0])
            # 'battlefield'
            #
            # 'centerhouse'
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
                if self.transition_target[0]=='room':
                    self.player.playerstat.key=True
                self.setup(self.tmx_maps[self.transition_target[0]],self.transition_target[1],self.transition_target[0])
                self.tint_mode='untint'
                self.transition_target=None
        self.tint_progress =max(0,min(self.tint_progress,255))
        self.tint_surf.set_alpha(self.tint_progress)
        self.display_surface.blit(self.tint_surf,(0,0))

    def black_out(self):
        while True:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type==pygame.QUIT:
                    sys.exit()
                if keys[pygame.K_SPACE]:
                    game.go()
            self.display_surface.fill('black')
            title_font=self.fonts['title']
            title_text = title_font.render("HOLES 고도형,이유진", True, COLORS['gold'])
            press_font=self.fonts['bold']
            press=press_font.render("press space to enter", True, COLORS['pure white'])
            self.display_surface.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 300))
            self.display_surface.blit(press, (WINDOW_WIDTH // 2 - press.get_width() // 2, 400))
            pygame.display.update()

    def go(self):
        while True:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type==pygame.QUIT:
                    sys.exit()
                if keys[pygame.K_SPACE]:
                    game.go2()
            self.display_surface.fill('black')
            title_font = self.fonts['explain']
            title_text1 = title_font.render("스탠리는 누명을 써서 이곳에 왔다.", True, COLORS['pure white'])
            title_text2 = title_font.render("여기는 뭐하는 곳일까?", True, COLORS['pure white'])
            title_text3 = title_font.render(".....", True, COLORS['pure white'])
            self.display_surface.blit(title_text1, (WINDOW_WIDTH // 2 - title_text1.get_width() // 2, 325))
            self.display_surface.blit(title_text2, (WINDOW_WIDTH // 2 - title_text2.get_width() // 2, 350))
            self.display_surface.blit(title_text3, (WINDOW_WIDTH // 2 - title_text3.get_width() // 2, 375))
            pygame.display.update()
    def go2(self):
        while True:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type==pygame.QUIT:
                    sys.exit()
                if keys[pygame.K_SPACE]:
                    game.run()
            self.display_surface.fill('black')
            title_font = self.fonts['Mr.sir']
            title_text1 = title_font.render("여긴 네가 새로운 사람이 될 수 있는 곳이다.", True, COLORS['pure white'])
            title_text2 = title_font.render("규칙만 잘 따라라.", True, COLORS['pure white'])
            self.display_surface.blit(title_text1, (WINDOW_WIDTH // 2 - title_text1.get_width() // 2, 325))
            self.display_surface.blit(title_text2, (WINDOW_WIDTH // 2 - title_text2.get_width() // 2, 375))

            pygame.display.update()
    def Go(self):
        while True:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type==pygame.QUIT:
                    sys.exit()
            print('aaa')



            self.display_surface.fill('black')

            title_font = self.fonts['explain']
            title_text1 = title_font.render("축하합니다", True, COLORS['pure white'])
            title_text2 = title_font.render("스탠리는 워든을 무찔렀습니다", True, COLORS['pure white'])
            title_text3 = title_font.render("보물상자는 많은 보물이 들어있었고 스탠리는 행복하게 살았다고 합니다", True, COLORS['pure white'])
            self.display_surface.blit(title_text1, (WINDOW_WIDTH // 2 - title_text1.get_width() // 2, 325))
            self.display_surface.blit(title_text2, (WINDOW_WIDTH // 2 - title_text2.get_width() // 2, 350))
            self.display_surface.blit(title_text3, (WINDOW_WIDTH // 2 - title_text3.get_width() // 2, 375))
            pygame.display.update()


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
                if self.index_open2:
                    self.traing_index.click1(event)
                    self.traing_index.click2(event)


                self.player.mousedbuttondown = True if event.type == pygame.MOUSEBUTTONDOWN else False
                self.player.mousedbuttonup = True if event.type == pygame.MOUSEBUTTONUP else False
            #updatedb
            if not self.player.gamestop:
                self.input()
                self.transition_check()
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
            elif self.index_open1:
                self.player_index.update(dt)
            elif self.index_open2:
                self.traing_index.update()
            else:
                # HP바
                draw_bar(
                    surface=self.display_surface,
                    rect=pygame.FRect(0, 0, 100, 20).move_to(
                        midbottom=Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 70)),
                    value=self.player.hp,
                    max_value=self.player.max_hp,
                    color=COLORS['red'],
                    bg_color=COLORS['white'],
                    radius=2)


            self.player.get_current_tool(self.tool_index.selected_tool)
            self.player_index.get_player(self.player)

            #땅파기 정도
            if self.key_down_time:
                draw_bar(
                surface=self.display_surface,
                rect=pygame.FRect(0,0,100,20).move_to(midbottom=Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-90)),
                value=pygame.time.get_ticks()-self.key_down_time,
                max_value=self.player.digtime,
                color=COLORS['white'],
                bg_color=COLORS['black']
            )


            if self.dialog_tree: self.dialog_tree.update()

            if pygame.key.get_just_pressed()[pygame.K_f]:
                self.player.coin+=1
                self.player.stat_update()

            if 0.0<=Game.k and Game.k<2.0:
                Game.k+=0.01
                rect_x, rect_y, rect_width, rect_height = 250, 600, 780, 80
                pygame.draw.rect(self.display_surface,COLORS['pure white'], (rect_x, rect_y, rect_width, rect_height))
                title_font = self.fonts['bold']
                title_text1 = title_font.render("여긴 네가 새로운 사람이 될 수 있는 곳이다.", True, COLORS['black'])
                self.display_surface.blit(title_text1, (WINDOW_WIDTH // 2 - title_text1.get_width() // 2, 620))
            elif 2.0<=Game.k and Game.k<4.0:
                Game.k += 0.01
                rect_x, rect_y, rect_width, rect_height = 250, 600, 780, 80
                pygame.draw.rect(self.display_surface, COLORS['pure white'], (rect_x, rect_y, rect_width, rect_height))
                title_font = self.fonts['bold']
                title_text1 = title_font.render("하루에 하나씩, 규격은 삽 한 개 길이다.", True, COLORS['black'])
                self.display_surface.blit(title_text1, (WINDOW_WIDTH // 2 - title_text1.get_width() // 2, 620))
            elif 4.0<=Game.k and Game.k<6.0:
                Game.k += 0.01
                rect_x, rect_y, rect_width, rect_height = 250, 600, 780, 80
                pygame.draw.rect(self.display_surface, COLORS['pure white'], (rect_x, rect_y, rect_width, rect_height))
                title_font = self.fonts['bold']
                title_text1 = title_font.render("모르는게 있을 때에는 항상 제로에게 가도록.", True, COLORS['black'])
                self.display_surface.blit(title_text1, (WINDOW_WIDTH // 2 - title_text1.get_width() // 2, 620))
            self.tint_screen(dt)
            if self.giant:
                if self.giant.get_live():

                    self.setup(self.tmx_maps['world'],'tent','world')
                    talk_rect = pygame.FRect(0, 0, WINDOW_WIDTH* 0.6, WINDOW_HEIGHT * 0.3).move_to(center=Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.7))

                    draw_text_in_box(self.display_surface,pygame.FRect(0,0,200,40).move_to(midleft=(WINDOW_WIDTH/2, WINDOW_HEIGHT)), COLORS['white'],self.fonts['regular'].render('드디어 돌연변이 고도형 닮은 노란색 도마뱀을 잡았따', False, COLORS['black']))

            pygame.display.update()
            if self.player.endgame:
                for group in (self.all_sprites, self.collision_sprites, self.transition_sprites):
                    group.empty()
                self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

                self.Go()







        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.black_out()

