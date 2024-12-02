import pygame

def scale(image, new_width):
    # Calculate the new height to maintain the aspect ratio
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height
    new_height = int(new_width / aspect_ratio)

    # Scale the image to the new dimensions
    scaled_image = pygame.transform.scale(image, (new_width, new_height))
    return scaled_image