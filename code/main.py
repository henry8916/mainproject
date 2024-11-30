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

        # tool
        self.player_tools={
            0:Tool('Shovel',1),
            1:Tool('Gun',0),
        }

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()

        # transition/tint
        self.transition_target = None
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_mode = 'untint'
        self.tint_progress = 0
        self.tint_direction=-1
        self.tint_speed = 600

        self.import_assets()
        self.setup(self.tmx_maps['world'],'tent')

        #overlay
        self.tool_index=ToolIndex(self.player_tools,self.fonts,self.tool_Frames)
        self.index_open=False

    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(join('holesmap', 'mainmap.tmx')), 'tent':load_pygame(join('holesmap', 'Tent.tmx')), 'wardenhouse':load_pygame(join('holesmap', 'Wardenhouse.tmx'))}

        self.tool_Frames={ 'icons': {'Shovel': pygame.image.load(join('icons','shovel-removebg-preview.png')).convert_alpha(),'Gun': pygame.image.load(join('icons','gun-removebg-preview.png')).convert_alpha()},
                           'tools': {}
        }
        print(self.tool_Frames['icons'])

        self.fonts={
            'dialog':pygame.font.Font(join('font','Moneygraphy-Rounded.ttf'),30),
            'regular':pygame.font.Font(join('font','Moneygraphy-Rounded.ttf'),18),
            'small':pygame.font.Font(join('font','Moneygraphy-Rounded.ttf'),14),
            'bold':pygame.font.Font(join('font','Moneygraphy-Rounded.ttf'),40),
            'explain': pygame.font.Font(join('font', 'Moneygraphy-Rounded.ttf'), 25)
        }


        #sprites
    def setup(self, tmx_map, player_start_pos):


        #map clear
        for group in (self.all_sprites, self.collision_sprites, self.transition_sprites):
            group.empty()


        for obj in tmx_map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x*2, obj.y*2),doublingimage(obj.image),(self.all_sprites, self.collision_sprites))

        #gound
        for x,y,image in tmx_map.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE), doublingimage(image), self.all_sprites)


        #collision sprite
        for obj in tmx_map.get_layer_by_name('Collision'):
            CollisionSprite((obj.x*2, obj.y*2),pygame.Surface((obj.width*2,obj.height*2)),self.collision_sprites)
        #transision
        for obj in tmx_map.get_layer_by_name('Transition'):
            # print(obj.properties)
            TransitionSprite((obj.x*2, obj.y*2),(obj.width*2,obj.height*2), (obj.properties['target'], obj.properties['pos']),self.transition_sprites)

        for obj in tmx_map.get_layer_by_name('Entities'):#타일드 멥 수정하기
            if obj.name =='Player' and obj.properties['pos']==player_start_pos:
                self.player = Player((obj.x*2, obj.y*2), self.all_sprites, self.collision_sprites)
                self.camera = Camera(self.player,self.all_sprites)
                # self.gun = Gun(self.player, self.all_sprites)


    def input(self):

        if pygame.key.get_just_pressed()[pygame.K_RETURN]:
            self.index_open = not self.index_open
            self.player.blocked=not self.player.blocked


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
                self.setup(self.tmx_maps[self.transition_target[0]],self.transition_target[1])
                self.tint_mode='untint'
                self.transition_target=None
        self.tint_progress =max(0,min(self.tint_progress,255))
        self.tint_surf.set_alpha(self.tint_progress)
        self.display_surface.blit(self.tint_surf,(0,0))


    def run(self):
        while self.running:
            #dt
            dt = self.clock.tick() / 1000
            self.display_surface.fill('black')
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            #update
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
            if self.index_open: self.tool_index.update(dt)



            self.tint_screen(dt)
            pygame.display.update()






        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()

