import pygame
from pygame.sprite import Sprite
from  bullet import Bullet
from scale_image import scale

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        org_img = scale(pygame.image.load('images/moong1.png'), ai_settings.ship_size)
        org_lac = scale(pygame.image.load('images/moong2.png'), ai_settings.ship_size)
        # Load the ship image and get its rect.
        self.image = org_img
        self.image_left = org_img
        self.lac_left = org_lac
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.lac_right = pygame.transform.flip(self.lac_left, True, False)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 5

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
        self.fire = False
        # Store last shot time
        self.last_shot_time = 0

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.center = self.screen_rect.center
        self.rect.bottom = self.screen_rect.bottom -5
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def lac(self):
        if self.image == self.image_left:
            self.image = self.lac_left
        if self.image == self.image_right:
            self.image = self.lac_right
    def no_lac(self):
        if self.image == self.lac_left:
            self.image = self.image_left
        if self.image == self.lac_right:
            self.image = self.image_right
    
    def update(self):
        """Update the ship's position, based on movement flags."""
        # Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ai_settings.ship_speed_factor
            self.image = self.image_right
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.ai_settings.ship_speed_factor
            self.image = self.image_left
        elif self.moving_up and self.rect.top > 0:
            self.y -= self.ai_settings.ship_speed_factor
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.ai_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)


