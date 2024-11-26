import pygame
from os.path import join
from os import walk

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
TILE_SIZE = 64

def doublingimage(image):
    original_width, original_height = image.get_size()
    scaled_image = pygame.transform.scale(image, (original_width * 2, original_height * 2))
    return scaled_image