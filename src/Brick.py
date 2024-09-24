import pygame
import random
from src.Dependency import *
from src.Powerups import PowerUp

class Brick:
    def __init__(self, x, y, color=1, tier=0):
        self.color = color  # Ensure this value is assigned
        self.tier = tier  # Ensure this value is assigned

        self.x=x
        self.y=y

        self.width = 96
        self.height = 48

        self.alive = True

        # Use get_brick_image to assign the correct image based on color and tier
        self.image = get_brick_image(self.color, self.tier)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def Hit(self, create_powerup_callback, is_ghost_mode=False):
        """Handles the logic when a brick is hit by the ball."""

        # Only play sound once per frame in ghost mode
        if is_ghost_mode and not self.alive:
            return  # Skip further logic if the brick is already destroyed in ghost mode
    
        # Decrease brick durability (based on color)
        if self.color == 1:
            self.alive = False  # Brick is destroyed when color reaches 1
        else:
            self.color = self.color - 1  # Reduce color (durability)

        # Play the appropriate sound
        if not self.alive:
            if not is_ghost_mode:  # Only play sound once if in ghost mode
                gSounds['brick-hit1'].play()

            # Power-up logic if the brick is destroyed
            if random.random() <= 0.15:
                # Define power-ups with weighted chances
                powerup_type = random.choices(
                    ["life", "paddle_widen", "ghost_ball", "catch_net", "laser_paddle"],
                    weights=[5, 35, 15, 30, 15],  # Adjust weights as needed
                    k=1
                )[0]  # Example weights: life has the lowest chance

                # Create power-up with the chosen type
                create_powerup_callback(self.x + self.width / 2, self.y, powerup_type)
                print(f"Log: Power-up triggered! Type: {powerup_type}")  # Logging for testing purposes
        else:
            if not is_ghost_mode:  # Avoid playing this sound multiple times in ghost mode
                gSounds['brick-hit2'].play()


    def update(self, dt):
        pass

    def render(self, screen):
        if self.alive:
            screen.blit(brick_image_list[((self.color-1)*4)+self.tier], (self.rect.x, self.rect.y))