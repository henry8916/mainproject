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
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()
        #sprites
    def setup(self):
        # map = load_pygame(join('data','maps','world.tmx'))
        holesmap = load_pygame(join('holesmap','mainmap.tmx'))
        for x,y,image in holesmap.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE), doublingimage(image), self.all_sprites)
        # for x,y,image in holesmap.get_layer_by_name('Collisionn').objects:
        #     Sprite((x*TILE_SIZE,y*TILE_SIZE), doublingimage(image), self.all_sprites)
        # for x,y,image in holesmap.get_layer_by_name('Objects').objects:
        #     Sprite((x*TILE_SIZE,y*TILE_SIZE), doublingimage(image), self.all_sprites)
        # for x,y,image in holesmap.get_layer_by_name('Transition').objects:
        #     Sprite((x*TILE_SIZE,y*TILE_SIZE), doublingimage(image), self.all_sprites)
        # for x,y,image in map.get_layer_by_name('Ground').tiles():
        #     Sprite((x*TILE_SIZE,y*TILE_SIZE), image, self.all_sprites)
        # for obj in map.get_layer_by_name('Objects'):
        #     CollisionSprite((obj.x, obj.y),obj.image,(self.all_sprites, self.collision_sprites))
        # for obj in holesmap.get_layer_by_name('Collision'):
        #     CollisionSprite((obj.x, obj.y),obj.image,(self.all_sprites, self.collision_sprites))
        for obj in holesmap.get_layer_by_name('Transition'):
            Sprite((obj.x, obj.y),obj.image,(self.all_sprites, self.collision_sprites))
        for obj in holesmap.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y),obj.image,(self.all_sprites, self.collision_sprites))

        # for obj in map.get_layer_by_name('Collisions'):
        #     CollisionSprite((obj.x,obj.y), pygame.Surface((obj.width,obj.height)),self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name =='Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.camera = Camera(self.player,self.all_sprites)
                # self.gun = Gun(self.player, self.all_sprites)

    def run(self):
        while self.running:
            #dt
            dt = self.clock.tick() / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            #update
            if not self.player.gamestop:
                self.all_sprites.update(dt)

            #draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.camera.pos,self.player)
            pygame.display.update()
            if self.player.timedelay:
                clock = pygame.time.get_ticks()
                while (pygame.time.get_ticks() - clock) < 200:
                    pass
                self.player.timedelay = False

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()

