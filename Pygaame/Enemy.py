import pygame

def UpdateEnemies(enemies, platform_list, current_time):
    # Initialize enemies on each platform if list is empty
    if not enemies:
        enemies = []
        for plat in platform_list:
            enemy_rect = pygame.Rect(plat.x + 40, plat.top - 40, 40, 40)
            enemies.append({
                "rect": enemy_rect,
                "spawned": True,
                "health": 30,
                "dx": 2,
                "platform": plat,
                "death_time": 0
            })

    # Update movement or handle respawn timers for each enemy
    for enemy_data in enemies:
        if not enemy_data["spawned"]:
            # Respawn after 5 seconds
            if current_time - enemy_data["death_time"] >= 5000:
                plat = enemy_data["platform"]
                enemy_data["rect"] = pygame.Rect(plat.x + 40, plat.top - 40, 40, 40)
                enemy_data["spawned"] = True
                enemy_data["health"] = 30
                enemy_data["dx"] = 2
        else:
            plat = enemy_data["platform"]
            rect = enemy_data["rect"]
            
            rect.x += enemy_data["dx"]
            
            # Platform edge boundary check and direction reversal
            if rect.left <= plat.left:
                rect.left = plat.left
                enemy_data["dx"] = 2
            elif rect.right >= plat.right:
                rect.right = plat.right
                enemy_data["dx"] = -2

    return enemies