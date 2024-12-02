import sys
from time import sleep
import pygame
from bullet import Bullet
from bullet import Enemy_Bullet
from alien import Alien
import random
from explosion import Explosion
from alien import Boss
from pygame.sprite import Sprite
re = []

def check_keydown_events(event, ship, stats):
    global re
    if event.key == pygame.K_q:
        filename = 'highscore.txt'
        with open(filename, 'w') as file_object:
            file_object.write(str(stats.high_score))
        sys.exit()
    if stats.game_active:
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_UP:
            ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            ship.fire = True


def start_game(ai_settings, screen, stats, ship, aliens, bullets, event, sb, enemy_bullets, explosions):
    if not stats.game_active:
        if event.key == pygame.K_RETURN:
            reset_game(ai_settings, screen, stats, ship, aliens,
                       bullets, sb, enemy_bullets, explosions)


def fire_bullet(ai_settings, screen, ship, bullets):
    current_time = pygame.time.get_ticks()
    if current_time - ship.last_shot_time >= ai_settings.shot_delay:
        # Create a new bullet and add it to the bullets group.
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)
            ship.last_shot_time = current_time
                
            ship.lac()
            pygame.time.set_timer(pygame.USEREVENT + 1, 100)


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_SPACE:
        ship.fire = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, enemy_bullets, explosions):
    if ship.fire:
        fire_bullet(ai_settings, screen, ship, bullets)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            filename = 'highscore.txt'
            with open(filename, 'w') as file_object:
                file_object.write(str(stats.high_score))
            sys.exit()
        elif event.type == pygame.USEREVENT + 1:
            # Revert the ship image back to the original
            ship.no_lac()    
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, stats)
            start_game(ai_settings, screen, stats, ship, aliens,
                       bullets, event, sb, enemy_bullets, explosions)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                              bullets, mouse_x, mouse_y, event, sb, enemy_bullets, explosions)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y, event, sb, enemy_bullets, explosions):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        reset_game(ai_settings, screen, stats, ship, aliens,
                   bullets, sb, enemy_bullets, explosions)

    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        reset_game(ai_settings, screen, stats, ship, aliens,
                   bullets, sb, enemy_bullets, explosions)


def reset_game(ai_settings, screen, stats, ship, aliens, bullets, sb, enemy_bullets, explosions):
    # Reset the game settings.
    ai_settings.initialize_dynamic_settings()

    # Reset the game statistics.
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True

    # Show resetted score
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    sb.prep_aliens_toKill()
    sb.show_score()

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
    enemy_bullets.empty()
    explosions.empty()

    # Create a new fleet and center the ship.
    alien_spawn(ai_settings, screen, ship, aliens, stats)
    ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, qs, enemy_bullets, game_over, explosions):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    explosions.draw(screen)
    update_explosions(explosions)

    # Draw the score information and print statement.
    sb.show_score()

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
        qs.show_quit()

    if game_over.over:
        aliens.empty()
        bullets.empty()
        ship.center_ship()
        game_over.draw_button()

    if stats.game_active:
        # Redraw alien bullets
        for enemy_bullet in enemy_bullets.sprites():
            enemy_bullet.draw_enemy_bullet()

        # Make the aliens shoot randomly
        if random.randrange(0, 2) == 1:
            alien_shoot(ai_settings, screen, aliens, enemy_bullets)

        # Check bullet-bullet collisions
        pygame.sprite.groupcollide(bullets, enemy_bullets, True, True)

        # Turn off game over flag
        game_over.over = False

    # Make sure the most recently drawn screen is visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, boss, bullets, explosions):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(
        ai_settings, screen, stats, sb, ship, aliens, boss, bullets, explosions)


def update_enemy_bullets(ai_settings, enemy_bullets):
    """Update position of enemy bullets"""
    enemy_bullets.update()
    for enemy_bullet in enemy_bullets.copy():
        if enemy_bullet.rect.top >= ai_settings.screen_height:
            enemy_bullets.remove(enemy_bullet)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, boss, bullets, explosions):
    """Respond to bullet-alien collisions"""
    if stats.level % ai_settings.boss_level == 0:
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
        if collisions:
            for bullet in collisions:
                explosion = Explosion(bullet.rect.x, bullet.rect.y, 2)
                explosions.add(explosion)
            boss.health -= 1
            if boss.health == 0:
                aliens.empty()
                stats.score += ai_settings.boss_points
                sb.prep_score()
                boss.health = ai_settings.boss_health
                
                # If the entire fleet is destroyed, start a new level
                
                bullets.empty()
                ai_settings.increase_speed()

                # Increase level.
                stats.level += 1
                sb.prep_level()
                sb.show_score()

                alien_spawn(ai_settings, screen, ship, aliens, stats)
            check_high_score(stats, sb)
    else:
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

        for alien in collisions:
            explosion = Explosion(alien.rect.centerx, alien.rect.centery, 2)
            explosions.add(explosion)
            stats.kills += 1

        if collisions:
            for alienss in collisions.values():
                stats.score += ai_settings.alien_points * len(alienss)
                sb.prep_score()
                sb.prep_aliens_toKill()                
            check_high_score(stats, sb)
                
        alien_spawn(ai_settings, screen, ship, aliens, stats)
        if stats.kills == ai_settings.aliens_toKill:
            # If the entire fleet is destroyed, start a new level
            stats.kills = 0
            
            bullets.empty()
            ai_settings.increase_speed()

            # Increase level.
            stats.level += 1
            aliens.empty()
            sb.prep_level()
            sb.prep_aliens_toKill()
            sb.show_score()

            alien_spawn(ai_settings, screen, ship, aliens, stats)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screens."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create and alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_boss(ai_settings, screen, aliens):
    '''Create a boss'''
    boss = Boss(ai_settings, screen)
    aliens.add(boss)


def alien_spawn(ai_settings, screen, ship, aliens, stats):
    if stats.level % ai_settings.boss_level == 0:
        if len(aliens) < 1:
            create_boss(ai_settings, screen, aliens)
    else:
        """Create aliens."""
        # Create the fleet of aliens.
        alien = Alien(ai_settings, screen)
        number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
        number_rows = get_number_rows(ai_settings, ship.rect.height,
                alien.rect.height)
        while (len(aliens) < ai_settings.aliens_allowed):
            alien_number = random.randint(0,number_aliens_x-1)
            row_number = random.randint(0,number_rows-1)
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_alien_edges(alien):
    """Respond appropriately if the alien have reached an edge."""
    if alien.check_edges():
        change_alien_direction(alien)


def change_alien_direction(alien):
    """Drop the entire fleet and change the fleet's direction"""
    alien.alien_direction *= -1


def ship_hit(stats, sb, ship, bullets, enemy_bullets, game_over, explosions):
    """Respond to ship being hit by alien or enemy bullet."""
    if stats.ships_left > 0:
        # Decrement ships left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Empty the list of bullets.
        bullets.empty()
        enemy_bullets.empty()
        explosions.empty()

        # Center the ship and move the aliens up.
        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        stats.ships_left = -1
        sb.prep_ships()
        stats.game_active = False
        pygame.mouse.set_visible(True)
        game_over.over = True


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button, qs, enemy_bullets, game_over, explosions):
    """Check if the fleet is at an edge, and then
    update the position of all aliens in the fleet."""
    for alien in aliens:
        check_alien_edges(alien)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        explosion = Explosion(ship.rect.centerx, ship.rect.centery, 3)
        explosions.add(explosion)
        update_screen(ai_settings, screen, stats, sb, ship, aliens,
                      bullets, play_button, qs, enemy_bullets, game_over, explosions)
        ship_hit(stats, sb, ship, bullets,
                 enemy_bullets, game_over, explosions)
    # Look for enemy bullet-ship collisions
    if pygame.sprite.spritecollideany(ship, enemy_bullets):
        explosion = Explosion(ship.rect.centerx, ship.rect.centery, 3)
        explosions.add(explosion)
        update_screen(ai_settings, screen, stats, sb, ship, aliens,
                      bullets, play_button, qs, enemy_bullets, game_over, explosions)
        ship_hit(stats, sb, ship, bullets,
                 enemy_bullets, game_over, explosions)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def load_score(stats):
    filename = 'highscore.txt'
    try:
        with open(filename) as file_object:
            score = file_object.read()
            stats.high_score = int(score)
    except FileNotFoundError:
        pass


def alien_shoot(ai_settings, screen, aliens, enemy_bullets):
    """Fire a bullet if limit is not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(enemy_bullets) < ai_settings.enemy_bullets_allowed:
        new_bullet = Enemy_Bullet(ai_settings, screen, aliens)
        enemy_bullets.add(new_bullet)


def update_explosions(explosions):
    # Update explosion positions
    explosions.update()
