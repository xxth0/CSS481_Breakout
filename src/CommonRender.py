from src.constants import *
from src.resources import *
import pygame

def RenderScore(screen, score):
    small_font = pygame.font.Font('./fonts/font.ttf', 24)
    t_score = small_font.render("Score:", False, (255, 255, 255))
    t_score_val = small_font.render(str(score), False, (255, 255, 255))
    
    # Adjust the y position to the bottom of the screen
    screen.blit(t_score, (WIDTH - 180, HEIGHT - 35))  # Adjust x for alignment
    rect = t_score_val.get_rect()
    rect.topright = (WIDTH - 40, HEIGHT - 35)  # Keep the same alignment for the score value
    screen.blit(t_score_val, rect)


def RenderHealth(screen, health):
    x_pos = 10  # Bottom left starting position
    y_pos = HEIGHT - 35  # Adjust to the bottom of the screen
    
    # Render filled hearts
    for i in range(health):
        screen.blit(sprite_collection["heart"].image, (x_pos, y_pos))
        x_pos += 33

    # Render empty hearts
    for i in range(3 - health):
        screen.blit(sprite_collection["empty_heart"].image, (x_pos, y_pos))
        x_pos += 33