import pygame
from src.constants import *
from src.Dependency import *

class PowerUp:
    def __init__(self, x, y, power_type):
        """Initialize the power-up with its position and type."""
        self.x = x
        self.y = y

        self.width = 32  # Size of the power-up
        self.height = 32
        self.power_type = power_type  # Type of power-ups
        self.alive = True

        # Power-up falling speed
        self.speed = 150

        # **Ensure rect is initialized for positioning and collision detection**
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
        self.power_type = power_type

        # Use the loaded powerup images based on type
        if self.power_type == "life":
            self.image = sprite_collection["powerups_heart"].image
        elif self.power_type == "paddle_widen":
            self.image = sprite_collection["powerups_widepaddle"].image
        elif self.power_type == "ghost_ball":
            self.image = sprite_collection["powerups_ghostball"].image
        elif self.power_type == "catch_net":
            self.image = sprite_collection["powerups_catchnet"].image
        elif self.power_type == "laser_paddle":
            self.image = sprite_collection["powerups_laser"].image


    def update(self, dt):
        """Update the power-up's position as it falls down."""
        if self.alive:
            self.y += self.speed * dt
            self.rect.y = self.y  # Update rect position based on y value

        # If the power-up falls off the screen, deactivate it
        if self.y > pygame.display.get_surface().get_height():
            self.alive = False

    def render(self, screen):
        """Render the power-up on the screen."""
        if self.alive:
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def activate(self, play_state):
        """Apply the power-up's effect when collected."""
        if self.power_type == "life":
            # Add one life, max 3
            if play_state.health < 3:
                play_state.health += 1
            gSounds['item'].set_volume(0.6)
            gSounds['item'].play()
            print("Log: Extra life gained!")  # For logging purposes

        elif self.power_type == "paddle_widen":
            play_state.widen_paddle(1.5, duration=20)
            gSounds['item'].play()   
            print("Log: Paddle widened for 20 seconds!")

        elif self.power_type == "ghost_ball":
            play_state.enable_ghost_ball(10)
            gSounds['item'].play()
            print("Log: Activate Ghost ball for 10 seconds!")

        elif self.power_type == "catch_net":
            play_state.enable_catch_net(10)
            gSounds['item'].play()
            print("Log: Catch net activated for 10 seconds!")

        elif self.power_type == "laser_paddle":
            play_state.enable_laser_paddle(10)
            gSounds['item'].play()
            print("Log: Laser paddle activated for 10 seconds!")

        self.alive = False