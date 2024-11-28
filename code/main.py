from settings import *
from player import *
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game:
    def __init__(self):
        #settings

        pygame.init()
        self.display_surface  = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Holes')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.trasition_sprites = pygame.sprite.Group()

        # transition/tint
        self.transiton_target = None
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_model = 'tint'
        self.tint_progress = 255
        self.tint_speed = 600

        self.import_assets()
        self.setup(self.tmx_maps['world'],'house')



    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(join('holesmap', 'mainmap.tmx'))}


        #sprites
    def setup(self, tmx_map, player_start_pos):

        for obj in tmx_map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x*2, obj.y*2),doublingimage(obj.image),(self.all_sprites, self.collision_sprites))

        #gound
        for x,y,image in tmx_map.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE), doublingimage(image), self.all_sprites)


        #collision sprite
        for obj in tmx_map.get_layer_by_name('Collision'):
            CollisionSprite((obj.x*2, obj.y*2),pygame.Surface((obj.width*2,obj.height*2)),self.collision_sprites)

        #transision
        # for obj in tmx_map.get_layer_by_name('Transition'):
        #     TransitionSprite((obj.x*2, obj.y*2),pygame.Surface((obj.width*2,obj.height*2)), (obj.properties['target'], obj.properties['pos']),self.trasition_sprites)


        for obj in tmx_map.get_layer_by_name('Entities'):#타일드 멥 수정하기
            if obj.name =='Player' and obj.properties['pos']=='tent':
                self.player = Player((obj.x*2, obj.y*2), self.all_sprites, self.collision_sprites)
                self.camera = Camera(self.player,self.all_sprites)
                # # self.gun = Gun(self.player, self.all_sprites)

    # transision system
    # def transition_check(self):
    #     sprites=[sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox_rect)]
    #     if sprites:
    #         self.player.block()
    #         self.transition_target=sprites[0].target
    #         self.tint_model='tint'
    #
    # def tint_screen(selfself,dt):
    #     if  self.tint_model=='tinit':
    #         self.tint_progress += self.tint_speed*d
    #
    #     self.tinit_surf.set_alpha(self.tint_progress)
    #     self.display_surface.blit(self.tint_surf,(0,0))

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
                self.all_sprites.update(dt)
                #self.transition_check()


            #draw
            self.all_sprites.draw(self.camera.pos,self.player)
            pygame.display.update()
            if self.player.timedelay:
                clock = pygame.time.get_ticks()
                while (pygame.time.get_ticks() - clock) < 200:
                    pass
                self.player.timedelay = False
            #overlays
            #if self.dialog_tree: self.dialog_tree.update()

            # self.tint_screen()
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()

