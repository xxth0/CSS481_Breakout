import pygame
from src.constants import *
from src.Dependency import *
from src.Brick import Brick  # Import the Brick class


class Ball:
    def __init__(self, skin=1):
        self.width = 24
        self.height = 24

        self.SetImage(skin)

        self.dx = 0
        self.dy = 0

        self.Reset()
        self.ghost_mode = False  # By default, ghost mode is off

    def SetImage(self, skin):
        self.skin = skin
        self.image = ball_image_list[self.skin-1]


    def set_ghost_mode(self, active):
        """Enable or disable ghost mode for the ball."""
        self.ghost_mode = active
        # Change the ball's appearance to indicate ghost mode
        if active:
            self.image = ball_image_list[4]  # Set ghost ball image
        else:
            self.image = ball_image_list[self.skin-1]  # Set to the original ball color


    def Collides(self, target):
        if self.rect.x > target.rect.x + target.width or target.rect.x > self.rect.x + self.width:
            return False

        if self.rect.y > target.rect.y + target.height or target.rect.y > self.rect.y + self.height:
            return False

        # If ghost mode is active and the target is a brick, destroy it without bouncing off
        if isinstance(target, Brick) and self.ghost_mode:
            target.Hit()  # Destroy the brick
            return True

        return True  # Normal collision handling for non-ghost mode


    def Reset(self):
        self.x = WIDTH/2 - 6
        self.y = HEIGHT/2 - 6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.dx = 0
        self.dy = 0


    def update(self, dt):
            self.rect.x += self.dx * dt
            self.rect.y += self.dy * dt

            #A ball hits a left wall
            if self.rect.x <= 0:
                self.rect.x = 0
                self.dx = -self.dx
                gSounds['wall-hit'].play()

            # A ball hits a right wall
            if self.rect.x >= WIDTH - 24:
                self.rect.x = WIDTH - 24
                self.dx = -self.dx
                gSounds['wall-hit'].play()

            # A ball hits a upper wall
            if self.rect.y <= 0:
                self.rect.y = 0
                self.dy = -self.dy
                gSounds['wall-hit'].play()

    def pass_through_bricks(self):
        """Pass through bricks, destroying them without bouncing off."""
        for brick in play_state.bricks:
            if self.rect.colliderect(brick.rect):
                brick.Hit(play_state)  # Destroy the brick without changing ball direction


    def render(self, screen):
        # rect.x rect.y is center?? or is it square box
        # rect = self.image.get_rect()
        # rect.center = (self.rect.x, self.rect.y)
        screen.blit(self.image, (self.rect.x, self.rect.y))
