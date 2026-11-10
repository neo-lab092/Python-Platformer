import pygame

def PlayerMovement(
    running, player, left_wall, right_wall, ground, ceiling, platform1, platform2, platform3, platform4, platform5, 
    jump_strength, player_y_velocity, is_jumping, is_fast_falling, player_x_velocity, dash_cooldown, events
):

    # dash cooldown timer
    if dash_cooldown > 0:
        dash_cooldown -= 1

    clicked = False
    mouse_released = False
    mouse_held = pygame.mouse.get_pressed()[0]

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                mouse_released = True

    keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # movement mods
    if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
        player_speed = 10
    else:
        player_speed = 5

    if keys[pygame.K_w] or keys[pygame.K_SPACE]:
        gravity = 0.2
    else:
        gravity = 1

    # jump trigger
    if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and not is_jumping:
        player_y_velocity = jump_strength
        is_jumping = True

    # fast fall 
    if keys[pygame.K_s]:
        is_fast_falling = True

    if is_fast_falling:
        player_speed = 0
        gravity = 5

    # horizontal movement, dashing with cooldown, and smooth knockback velocity application
    previous_player_x = player.x

    if player_x_velocity != 0:
        player.x += int(player_x_velocity)
        player_x_velocity *= 0.85  # Friction decay factor (slows down smoothly)
        if abs(player_x_velocity) < 0.5:
            player_x_velocity = 0
            
    if keys[pygame.K_a]:
        player.x -= player_speed
    if keys[pygame.K_d]:
        player.x += player_speed

    # Dash ability (requires LALT + A or D, and dash_cooldown must be 0)
    if dash_cooldown == 0:
        if keys[pygame.K_a] and keys[pygame.K_LALT]:
            player_x_velocity = -22  # Dash burst speed left
            dash_cooldown = 45       # Cooldown frames (~0.75 seconds)
        elif keys[pygame.K_d] and keys[pygame.K_LALT]:
            player_x_velocity = 22   # Dash burst speed right
            dash_cooldown = 45       # Cooldown frames

    # Boundaries and vertical physics
    player.x = max(left_wall.right, min(player.x, right_wall.left - player.width))
    player_y_velocity += gravity
    player.y += player_y_velocity

    # Stop the player at the sides of platforms.
    platforms = (platform1, platform2, platform3, platform4, platform5)
    horizontal_movement = player.x - previous_player_x
    if horizontal_movement > 0:
        for platform in platforms:
            if (
                player.colliderect(platform)
                and previous_player_x + player.width <= platform.left
            ):
                player.right = platform.left
    elif horizontal_movement < 0:
        for platform in platforms:
            if (
                player.colliderect(platform)
                and previous_player_x >= platform.right
            ):
                player.left = platform.right

    # Collisions
    if player_y_velocity > 0 and player.colliderect(ground):
        player.bottom = ground.top
        player_y_velocity = 0
        is_jumping = False
        is_fast_falling = False
    elif player_y_velocity < 0 and player.colliderect(ceiling):
        player.top = ceiling.bottom
        player_y_velocity = 0
    elif player_y_velocity > 0 and player.colliderect(left_wall):
        player.bottom = left_wall.top
        player_y_velocity = 0
    elif player_y_velocity > 0 and player.colliderect(right_wall):
        player.bottom = right_wall.top
        player_y_velocity = 0
    else:
        for platform in platforms:
            if not player.colliderect(platform):
                continue

            if player_y_velocity > 0:
                if player.bottom - player_y_velocity <= platform.top + 10:
                    player.bottom = platform.top
                    player_y_velocity = 0
                    is_jumping = False
                    is_fast_falling = False
                break
            if player_y_velocity < 0:
                if player.top - player_y_velocity >= platform.bottom - 10:
                    player.top = platform.bottom
                    player_y_velocity = 0
                break

    return running, player_y_velocity, is_jumping, is_fast_falling, mouse_x, mouse_y, mouse_held, mouse_released, player_x_velocity, dash_cooldown