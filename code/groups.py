
from settings import *
#draw 함수 즉 모든 이미지를 그리는 함수
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