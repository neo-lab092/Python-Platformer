import pygame
import sys
from Environment1 import Environment1
from PlayerMovement import PlayerMovement
from Enemy import UpdateEnemies
from Projectiles import HandleWeaponAndProjectiles

pygame.init()

pygame.font.init()
font = pygame.font.SysFont('consolas', 30)
title_font = pygame.font.SysFont('consolas', 50)
fps_counter = pygame.time.Clock()

screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Platformer Game")

clock = pygame.time.Clock()

ground, ceiling, left_wall, right_wall, platform1, platform2, platform3, platform4, platform5 = Environment1(screen_width, screen_height)
platforms_tuple = (platform1, platform2, platform3, platform4, platform5)

game_state = "MENU"

def reset_game():
    global player, player_speed, gravity, jump_strength, player_y_velocity, player_x_velocity
    global is_jumping, is_fast_falling, score, player_health, enemies, enemy_killed
    global charge_time, projectile, proj_dx, proj_dy, explosion_timer, explosion_x, explosion_y
    global proj_is_charged, player_hit_cooldown, dash_cooldown

    player = pygame.Rect(100, 100, 50, 50)
    player_speed = 5 #def 5 
    gravity = 1 #def 1
    jump_strength = -10 # def -10
    player_y_velocity = 0
    player_x_velocity = 0
    is_jumping = False
    is_fast_falling = False

    score = 0
    player_health = 100 # def 100
    enemy_killed = 0
    enemies = []

    charge_time = 0
    projectile = None
    proj_dx = 0
    proj_dy = 0
    explosion_timer = 0
    explosion_x = 0
    explosion_y = 0
    proj_is_charged = False
    player_hit_cooldown = 0
    dash_cooldown = 0

reset_game()

running = True
mouse_x, mouse_y = 0, 0

while running:
    mouse_held = pygame.mouse.get_pressed()[0]
    events = pygame.event.get()
    
    # for menu screens
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = "PLAYING"
            elif game_state in ["WIN", "GAME_OVER"]:
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_ESCAPE:
                    game_state = "MENU"

    # Menu state view
    if game_state == "MENU":
        screen.fill((0, 102, 204))
        
        title_text = title_font.render("TESTGAME1", True, (100, 220, 255))
        start_text = font.render("Enter to start", True, (255, 255, 255))
        controls_text1 = font.render("Controls: A/D to Move, W/Space to Jump, LSHIFT to Sprint", True, (200, 200, 200))
        controls_text2 = font.render("LALT + A/D to Dash, LClick to shoot, Hold LClick to charge", True, (200, 200, 200))
        goal_text = font.render("Reach: 300", True, (255, 215, 0))

        left_x = 60
        screen.blit(title_text, (left_x, 180))
        screen.blit(start_text, (left_x, 280))
        screen.blit(goal_text, (left_x, 350))
        screen.blit(controls_text1, (left_x, 450))
        screen.blit(controls_text2, (left_x, 490))

    # Playing loop state
    elif game_state == "PLAYING":
        running, player_y_velocity, is_jumping, is_fast_falling, mouse_x, mouse_y, mouse_held, mouse_released, player_x_velocity, dash_cooldown = PlayerMovement(
            running, player, left_wall, right_wall, ground, ceiling, platform1, platform2, platform3, platform4, platform5,
            jump_strength, player_y_velocity, is_jumping, is_fast_falling, player_x_velocity, dash_cooldown, events
        )

        # Smooth knockback momentum decay
        if player_x_velocity != 0:
            player.x += int(player_x_velocity)
            player_x_velocity *= 0.85  
            if abs(player_x_velocity) < 0.5:
                player_x_velocity = 0

        # Update enemies across all platforms
        enemies = UpdateEnemies(enemies, platforms_tuple, pygame.time.get_ticks())

        # Projectile system update
        projectile, proj_dx, proj_dy, charge_time, enemies, score, explosion_timer, explosion_x, explosion_y, proj_is_charged, enemy_killed = HandleWeaponAndProjectiles(
            mouse_held, mouse_released, mouse_x, mouse_y, player,
            charge_time, projectile, proj_dx, proj_dy,
            enemies, score,
            ground, ceiling, left_wall, right_wall, platform1, platform2, platform3, platform4, platform5,
            explosion_timer, explosion_x, explosion_y, proj_is_charged, enemy_killed
        )

        # invunriblity frames
        if player_hit_cooldown > 0:
            player_hit_cooldown -= 1

        # player enemy colision
        for enemy_data in enemies:
            if enemy_data["spawned"] and enemy_data["rect"] is not None:
                if player.colliderect(enemy_data["rect"]) and player_hit_cooldown == 0:
                    player_health -= 20
                    player_hit_cooldown = 60
                    print(f"Dmg player: {player_health}")
                    
                    dx = player.centerx - enemy_data["rect"].centerx
                    dy = player.centery - enemy_data["rect"].centery

                    if dx < 0:
                        player_x_velocity = -12
                    else:
                        player_x_velocity = 12

                    if dy > 0:  
                        player_y_velocity = -8
                    break

        # Win / Lose condition checks
        if score >= 300:
            game_state = "WIN"
        elif player_health <= 0:
            game_state = "GAME_OVER"

        # Clear screen and draw environment
        screen.fill((40, 42, 54))

        pygame.draw.rect(screen, (80, 80, 100), ground)
        pygame.draw.rect(screen, (80, 80, 100), ceiling)
        pygame.draw.rect(screen, (80, 80, 100), left_wall)
        pygame.draw.rect(screen, (80, 80, 100), right_wall)

        pygame.draw.rect(screen, (100, 100, 100), platform1)
        pygame.draw.rect(screen, (100, 100, 100), platform2)
        pygame.draw.rect(screen, (100, 100, 100), platform3)
        pygame.draw.rect(screen, (100, 100, 100), platform4)
        pygame.draw.rect(screen, (1, 1, 1), platform5)

        # Player flash feedback during invulnerability frames
        if player_hit_cooldown > 0 and (player_hit_cooldown // 5) % 2 == 0:
            pygame.draw.rect(screen, (255, 255, 255), player)
        else:
            pygame.draw.rect(screen, (255, 80, 80), player)

        # alive enemies
        for enemy_data in enemies:
            if enemy_data["spawned"] and enemy_data["rect"] is not None:
                pygame.draw.rect(screen, (80, 255, 80), enemy_data["rect"])

        # render proj
        if projectile is not None:
            if charge_time > 30:
                pygame.draw.circle(screen, (255, 69, 0), (int(projectile.centerx), int(projectile.centery)), 14)
            else:
                pygame.draw.circle(screen, (255, 255, 0), (int(projectile.centerx), int(projectile.centery)), 8)

        # render explosio effect
        if explosion_timer > 0:
            pygame.draw.circle(screen, (255, 120, 0), (int(explosion_x), int(explosion_y)), 60, 3)

        # aiming line
        player_center = (player.centerx, player.centery)
        pygame.draw.line(screen, (255, 255, 0), player_center, (mouse_x, mouse_y), 5)

        # HUD UI
        fps_text = font.render(f"FPS: {round(clock.get_fps())}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        health_text = font.render(f"Health: {player_health}", True, (255, 80, 80) if player_health <= 30 else (255, 255, 255))
        screen.blit(health_text, (10, 40))

        score_text = font.render(f"Score: {score} / 300", True, (100, 220, 255))
        screen.blit(score_text, (10, 70))

        Charge_text = font.render(f"Charge:  {charge_time}", True, (255 ,80 ,80))
        screen.blit(Charge_text, (10, 100))

    # WIN screen
    elif game_state == "WIN":
        screen.fill((255, 255, 255))
        win_title = title_font.render("Win", True, (100, 255, 100))
        restart_text = font.render("press R to go again, Esc for menu", True, (0, 0, 0))
        
        screen.blit(win_title, (screen_width // 2 - win_title.get_width() // 2, 250))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, 350))

    # LOSE screen
    elif game_state == "GAME_OVER":
        screen.fill((0, 0, 0))
        lose_title = title_font.render("lose", True, (255, 80, 80))
        restart_text = font.render("press R to go again, Esc for menu", True, (255, 255, 255))
        final_score = font.render(f"Final Score: {score}", True, (255, 255, 255))

        screen.blit(lose_title, (screen_width // 2 - lose_title.get_width() // 2, 220))
        screen.blit(final_score, (screen_width // 2 - final_score.get_width() // 2, 290))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, 360))

    pygame.display.flip()
    clock.tick(60) #def 60, max frame cap

pygame.quit()
sys.exit()