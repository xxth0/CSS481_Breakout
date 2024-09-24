import pygame
from src.constants import *
from src.Dependency import *

class Paddle:
    def __init__(self, skin=1):
        self.x = WIDTH/2 - 96
        self.y = HEIGHT - 96

        self.dx = 0

        self.size = 2

        self.width = self.size * 96 # 2 * 32 * 3 (scale)
        self.height = 48   # 16 * 3 (scale)

        self.SetImage(skin)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def SetImage(self, skin):
        self.skin = skin
        self.image = paddle_image_list[self.skin-1]

    def widen(self, multiplier):
        """Widen the paddle by a multiplier (e.g., 1.5x) and update the image."""
        self.size *= 1.5
        self.width = self.size * 96
        self.rect.width = self.width  # Update the rect to match the new width

        # **Stretch the paddle image to match the new width**
        self.image = pygame.transform.scale(widened_paddle_image_list[self.skin - 1], (self.width, self.height))


    def restore(self):
        """Restore the paddle to its original size and update the image."""
        self.size /= 1.5
        self.width = self.size * 96
        self.rect.width = self.width  # Update the rect to match the original width

        # **Restore the original image size**
        self.image = pygame.transform.scale(paddle_image_list[self.skin - 1], (self.width, self.height))


    def update(self, dt):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.dx = -PADDLE_SPEED
        elif key[pygame.K_RIGHT]:
            self.dx = PADDLE_SPEED
        else:
            self.dx = 0

        if self.dx < 0:
            self.rect.x = max(0, self.rect.x + self.dx * dt)
        else:
            self.rect.x = min(WIDTH - self.width, self.rect.x + self.dx * dt)


    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))