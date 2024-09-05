import pygame


def crop_image(image: pygame.Surface) -> pygame.Surface:
    """
    Crop the image to the smallest bounding rectangle.

    :param image: Image to crop
    :return: Cropped image
    """

    mask = pygame.mask.from_surface(image, threshold=1)

    return image.subsurface(mask.get_bounding_rects()[0]).copy()
