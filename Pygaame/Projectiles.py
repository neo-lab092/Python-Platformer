import pygame
import math

_projectile_damage = 15

def HandleWeaponAndProjectiles(
    mouse_held, mouse_released, mouse_x, mouse_y, player, charge_time, projectile, proj_dx, proj_dy, enemies, score, ground, ceiling, left_wall, right_wall, platform1, platform2, platform3, platform4, platform5,
    explosion_timer, explosion_x, explosion_y, proj_is_charged, enemy_killed
):
    global _projectile_damage

    # Decrease explosion visual timer
    if explosion_timer > 0:
        explosion_timer -= 1

    # Charge weapon when holding mouse click
    if mouse_held and projectile is None:
        charge_time += 1 
        if charge_time > 60: #def 60
            charge_time = 60

    # Fire projectile on mouse release
    if mouse_released and projectile is None:
        proj_x = player.centerx
        proj_y = player.centery
        projectile = pygame.Rect(proj_x - 8, proj_y - 8, 16, 16)

        angle = math.atan2(mouse_y - proj_y, mouse_x - proj_x)
        speed = 30 #def 12
        proj_dx = speed * math.cos(angle)
        proj_dy = speed * math.sin(angle)

        if charge_time > 15:
            proj_is_charged = True
            current_damage = int(5 + (charge_time / 60) * 40)
            proj_damage = min(current_damage, 50)
        else:
            proj_is_charged = False
            proj_damage = 5

        _projectile_damage = proj_damage
        charge_time = 0
    else:
        proj_damage = 0

    explosion_radius = 60
    projectile_exploded = False

    # Move projectile and check collisions
    if projectile is not None:
        projectile.x += proj_dx
        projectile.y += proj_dy

        hit_target = False
        for enemy_data in enemies:
            if enemy_data["spawned"] and enemy_data["rect"] is not None and projectile.colliderect(enemy_data["rect"]):
                hit_target = True
                break

        environment_elements = (ground, ceiling, left_wall, right_wall, platform1, platform2, platform3, platform4, platform5)
        for element in environment_elements:
            if projectile.colliderect(element):
                hit_target = True
                break

        if hit_target or projectile.x < 0 or projectile.x > 1280 or projectile.y < 0 or projectile.y > 720:
            projectile_exploded = True

        # Handle explosion effects or direct damage on impact
        if projectile_exploded:
            if proj_is_charged:
                explosion_x = projectile.centerx
                explosion_y = projectile.centery
                explosion_timer = 12  

                for enemy_data in enemies:
                    if enemy_data["spawned"] and enemy_data["rect"] is not None:
                        dist_x = projectile.centerx - enemy_data["rect"].centerx
                        dist_y = projectile.centery - enemy_data["rect"].centery
                        distance = math.sqrt(dist_x ** 2 + dist_y ** 2)
                        
                        if distance <= explosion_radius:
                            enemy_data["health"] -= _projectile_damage
                            print(f"Charged Explosion hit: {_projectile_damage} D HP left: {enemy_data['health']}")
                            if enemy_data["health"] <= 0:
                                enemy_data["spawned"] = False
                                enemy_data["rect"] = None
                                enemy_data["death_time"] = pygame.time.get_ticks()
                                enemy_killed += 1
                                score += 30
            else:
                for enemy_data in enemies:
                    if enemy_data["spawned"] and enemy_data["rect"] is not None and projectile.colliderect(enemy_data["rect"]):
                        enemy_data["health"] -= _projectile_damage
                        print(f"Standard hit: {_projectile_damage} damage. Remaining HP: {enemy_data['health']}")
                        if enemy_data["health"] <= 0:
                            enemy_data["spawned"] = False
                            enemy_data["rect"] = None
                            enemy_data["death_time"] = pygame.time.get_ticks()
                            enemy_killed += 1
                            score += 10
                        break

            projectile = None
                
    return projectile, proj_dx, proj_dy, charge_time, enemies, score, explosion_timer, explosion_x, explosion_y, proj_is_charged, enemy_killed