import pygame


def crop_image(image):
    mask = pygame.mask.from_surface(image, threshold=1)

    return image.subsurface(mask.get_bounding_rects()[0]).copy()
