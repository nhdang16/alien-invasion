class Settings():
    """A class to store all settings for Alien invasion"""

    def __init__(self):
        """Initialize the game's static settings"""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (0, 0, 0)
        # Ship settings
        self.ship_limit = 3
        self.ship_size = 60

        # Bullet settings
        self.bullet_width = 8
        self.bullet_height = 15
        self.alien_bullet_width = 5
        self.alien_bullet_height = 15
        self.bullets_allowed = 3

        # Enemy bullet settings
        self.enemy_bullet_color = 255,255,255
        self.enemy_bullets_allowed = 3

        # Alien settings
        self.alien_size = 50
        self.aliens_allowed = 10
        self.aliens_toKill = 20


        # Boss settings

        self.boss_size = 250
        self.boss_level = 2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 20
        self.boss_speed_factor = 3     
        self.alien_speed_factor = 3
        self.shot_delay = 250
        self.boss_health = 30
        self.enemy_bullet_speed_factor = 5

        # Scoring
        self.alien_points = 50
        self.boss_points = 1000
        # How quickly the game speeds up.
        self.speed_up_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speed_up_scale
        self.bullet_speed_factor *= self.speed_up_scale
        self.alien_speed_factor *= self.speed_up_scale
        self.boss_speed_factor *= self.speed_up_scale
        self.enemy_bullet_speed_factor *= self.speed_up_scale
        self.aliens_allowed += 3
        self.aliens_toKill += 5

        self.alien_points = int(self.alien_points * self.score_scale)


