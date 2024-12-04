import pygame
from os.path import join
from os import walk


WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
TILE_SIZE = 64
ANIMATION_SPEED=6
def doublingimage(image):
    original_width, original_height = image.get_size()
    scaled_image = pygame.transform.scale(image, (original_width * 2, original_height * 2))
    return scaled_image

def smallerimage(image):
    original_width, original_height = image.get_size()
    scaled_image = pygame.transform.scale(image, (original_width * 128 / 500, original_height * 128 / 500 ))
    return scaled_image

def smallerimage2(image):
    original_width, original_height = image.get_size()
    scaled_image = pygame.transform.scale(image, (original_width * 128 / 300, original_height * 128 / 300 ))
    return scaled_image

def rescaleimage(image,first, later):
    original_width, original_height = image.get_size()
    scaled_image = pygame.transform.scale(image, (original_width * later / first, original_height * later / first ))
    return scaled_image

COLORS = {
	'white': '#f4fefa',
	'pure white': '#ffffff',
	'dark': '#2b292c',
	'light': '#c8c8c8',
	'gray': '#3a373b',
	'gold': '#ffd700',
	'light-gray': '#4b484d',
	'fire':'#f8a060',
	'water':'#50b0d8',
	'plant': '#64a990',
	'black': '#000000',
	'red': '#f03131',
	'blue': '#66d7ee'
}

