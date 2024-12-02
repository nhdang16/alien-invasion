import pygame
from pygame.sprite import Sprite
from scale_image import scale
import random

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    # Store alien images
    alien_images = []
    for num in range(1, 13):
        img = pygame.image.load(f"images/alien{num}.png")
        alien_images.append(img)
    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute.
        self.image_right = scale(random.choice(self.alien_images),ai_settings.alien_size)
        self.image_left = pygame.transform.flip(self.image_right,True,False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        
        self.alien_direction = random.choice([1,-1])
        # store the alien's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right - 10:
            return True
        elif self.rect.left <= 10:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += self.ai_settings.alien_speed_factor * self.alien_direction
        self.rect.x = self.x
        if self.alien_direction == 1:
            self.image = self.image_right
        if self.alien_direction == -1:
            self.image = self.image_left
class Boss(Sprite):
    # Store boss images
    boss_images = []
    for num in range(1, 5):
        img = pygame.image.load(f"images/boss{num}.png")
        boss_images.append(img)
    def __init__(self, ai_settings,screen):
        """Initialize the Boss and set its starting position."""
        super(Boss, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Load the Boss image and get its rect.
        self.image_right = scale(random.choice(self.boss_images),ai_settings.boss_size)
        self.image_left = pygame.transform.flip(self.image_right,True,False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Start boss near the top left of the screen.
        self.rect.x = self.screen_rect.centerx
        self.rect.y = self.screen_rect.top
        
        self.alien_direction = random.choice([1,-1])
        # Store the boss' exact position.
        self.x = float(self.rect.x)
        self.health = self.ai_settings.boss_health
    def center_Boss(self):
        """Center the Boss on the screen."""
        self.center = self.screen_rect.centerx    
    def blitme(self):
        """Draw the Boss at its current location."""
        self.screen.blit(self.image, self.rect)
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    def update(self):
        """Move the boss right or left."""
        self.x += self.ai_settings.boss_speed_factor*self.alien_direction
        self.rect.x = self.x
        if self.alien_direction == 1:
            self.image = self.image_right
        if self.alien_direction == -1:
            self.image = self.image_left


