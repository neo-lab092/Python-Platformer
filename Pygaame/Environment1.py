import pygame

def Environment1(screen_width, screen_height):
    # environment elements
    ground = pygame.Rect(0, 620, screen_width, 100)
    ceiling = pygame.Rect(0, 0, screen_width, 100)
    left_wall = pygame.Rect(-95, 0, 100, screen_height)
    right_wall = pygame.Rect(1275, 0, 100, screen_height)

    platform1 = pygame.Rect(300, 500, 300, 25)
    platform2 = pygame.Rect(700, 400, 300, 25)
    platform3 = pygame.Rect(1000, 300, 200, 25)
    platform4 = pygame.Rect(200, 200, 200, 25)
    platform5 = pygame.Rect(300, 320, 400, 25)  

    return ground, ceiling, left_wall, right_wall, platform1, platform2, platform3, platform4, platform5
