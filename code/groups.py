
from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self,target_pos,player):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH/2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT/2)

        ground_sprites = [sprite for sprite in self if hasattr(sprite,'ground') and sprite.rect != None]
        object_sprites = [sprite for sprite in self if not hasattr(sprite,'ground') and sprite.rect != None]
        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect.topleft+self.offset)


    # def draw(self, player):
    #     self.offset.x = -(player.rect.centerx - WINDOW_WIDTH / 2)
    #     self.offset.y = -(player.rect.centery - WINDOW_HEIGHT / 2)
    #
    #     bg_sprites = [sprite for sprite in self if sprite.z < WORLD_LAYERS['main']]
    #     main_sprites = sorted([sprite for sprite in self if sprite.z == WORLD_LAYERS['main']],
    #                           key=lambda sprite: sprite.y_sort)
    #     fg_sprites = [sprite for sprite in self if sprite.z > WORLD_LAYERS['main']]
    #
    #     for layer in (bg_sprites, main_sprites, fg_sprites):
    #         for sprite in layer:
    #             if isinstance(sprite, Entity):
    #                 self.display_surface.blit(self.shadow_surf, sprite.rect.topleft + self.offset + vector(40, 110))
    #             self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
    #             if sprite == player and player.noticed:
    #                 rect = self.notice_surf.get_frect(midbottom=sprite.rect.midtop)
    #                 self.display_surface.blit(self.notice_surf, rect.topleft + self.offset)